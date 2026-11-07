# Python UI Automation & Reliability Framework

A Python/Playwright testing project built around a small ticket-desk application. The app runs locally so I can reproduce browser timing, validation and localization problems without depending on a third-party service.

I also test the public [Playwright TodoMVC demo](https://demo.playwright.dev/todomvc/) to check the same testing setup against a separate application.

## What's included

- **UI regression tests:** search, ticket creation, status changes, form validation, keyboard navigation and TodoMVC task workflows
- **Localization checks:** English/French labels and Irish/French date and currency formats
- **Reliability experiment:** compare a fixed sleep with a condition-based Playwright assertion during controlled slow search updates
- **Debugging evidence:** Pytest HTML reports, failure screenshots and Playwright traces
- **CI:** GitHub Actions runs local tests in Chromium and external TodoMVC tests in Chromium and Firefox

## Run the tests

Install Python 3.11+ and create a virtual environment.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
```

Run the local tests (no external website required):

```bash
python -m pytest -q -m "not external" --html=report.html --self-contained-html
```

Run the external TodoMVC tests (internet required):

```bash
python -m pytest -q -m external
```

For Firefox, install it first with `python -m playwright install firefox` and set `PLAYWRIGHT_BROWSER=firefox`. GitHub Actions runs both browsers automatically.

To inspect the ticket desk in a browser:

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory sample_app
```

Open `http://127.0.0.1:8000` and try the language selector, search, and Resolve/Reopen buttons.

## Reliability experiment

```bash
python -m scripts.reliability_experiment --iterations 12
```

The script deliberately sets search delays of 20 ms and 260 ms. In [this CI run](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371084086), a fixed 100 ms wait passed **6/12** runs, while the condition-based assertion passed **12/12**.

These are measured results for an injected delay, not a production performance benchmark. Raw results are written to `artifacts/reliability.json`.

## Bugs investigated

| Case | What failed | Fix |
| --- | --- | --- |
| Long ticket title on mobile | The page overflowed at 360px width | Wrap long unbroken titles |
| Whitespace-only form input | Blank tickets were created | Validate trimmed values and show an error |
| Keyboard Resolve/Reopen | Focus disappeared when a button was replaced | Restore focus to the updated button or status filter |

See [debugging notes](docs/DEBUGGING_WALKTHROUGH.md) for failing/passing CI runs, test files and the reasoning behind each fix.

Two separate test cases also enable deliberately incorrect French labels and currency formatting. They assert the exact incorrect output with fault injection enabled and the correct output without it.

## Latest CI result

[Main-branch test run](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42375140181): **32 local tests passed**, **8 TodoMVC tests passed in Chromium**, and **8 passed in Firefox** (40 test executions, including the same eight external scenarios run twice).

Browse the test code in [`tests/`](tests/), the timing experiment in [`scripts/`](scripts/), and the CI workflow in [`.github/workflows/`](.github/workflows/). Development decisions and previous runs are retained in [`DEVELOPMENT_LOG.md`](DEVELOPMENT_LOG.md).

**Scope:** Browser UI testing, not native iOS/macOS automation. The local app and its injected defects are test fixtures, not a production customer system.
