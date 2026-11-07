import os

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
        browser = playwright.chromium.launch(**options)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    try:
        yield page
    finally:
        context.close()
