import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from test_support.server import serve_app


@pytest.fixture(scope="session")
def app_url():
    with serve_app() as url:
        yield url


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        options = {"headless": True}
        executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        if executable:
            options["executable_path"] = executable
        name = os.environ.get("PLAYWRIGHT_BROWSER", "chromium")
        if name not in {"chromium", "firefox"}:
            raise ValueError(f"Unsupported test browser: {name}")
        browser = getattr(playwright, name).launch(**options)
        try:
            yield browser
        finally:
            browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"report_{report.when}", report)


@pytest.fixture
def page(browser, request):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    try:
        yield page
    finally:
        result = getattr(request.node, "report_call", None)
        # Negative controls represent deliberately seeded defects.
        # Retain their traces even when the assertions correctly detect them.
        failed = (
            (result is not None and result.failed)
            or request.node.get_closest_marker("negative_control") is not None
        )
        if failed:
            name = re.sub(r"[^a-zA-Z0-9_-]+", "_", request.node.nodeid)[:130]
            directory = Path(os.environ.get("UI_TEST_ARTIFACT_DIR", "artifacts/failures"))
            directory.mkdir(parents=True, exist_ok=True)
            try:
                page.screenshot(path=str(directory / f"{name}.png"), full_page=True)
            except Exception as error:
                print(f"Could not capture screenshot for {name}: {error}")
            try:
                context.tracing.stop(path=str(directory / f"{name}.zip"))
            except Exception as error:
                print(f"Could not capture browser trace for {name}: {error}")
        else:
            context.tracing.stop()
        context.close()
