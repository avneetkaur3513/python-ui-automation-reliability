# Python UI Automation & Reliability Framework

This project explores a practical testing question: what makes a browser test reliable, and what information helps when it fails?

It uses a small ticket-desk app that runs locally. Having control over the app makes it possible to repeat timing and localization problems without relying on a public website changing underneath the tests.

The focus is on Python, Playwright, Pytest, debugging and test evidence. There is no AI service or dashboard.

## What it tests

- Searching, creating, resolving and reopening tickets
- Required fields, empty states, case-insensitive search and unusual input
- English/French labels and Irish/French date and currency formatting
- Asynchronous search updates and rapid input changes
- Narrow mobile layouts, including long unbroken text
- Two deliberately seeded localization defects (marked as expected failures)

Each test starts with a new browser context; the data in the app resets on page load.

## Run locally

Python 3.11+ and a working Chromium installation are needed.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m pytest -q --html=report.html --self-contained-html
```

To reproduce the timing investigation:

```bash
python -m scripts.reliability_experiment --iterations 12
```

That script tests two approaches against deliberately delayed search updates: an arbitrary fixed wait and an assertion that waits for the expected state. It saves the actual observations in `artifacts/reliability.json`.

## What the experiment showed

In GitHub Actions [run 42371084086](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371084086):

| Test approach | Passed |
| --- | ---: |
| Fixed 100 ms wait | 6 / 12 |
| Wait for expected result | 12 / 12 |

The delay alternates between 20 ms and 260 ms. This is an **injected timing experiment**, not a claim that a production system has random failures. It demonstrates why fixed waits can produce unstable tests.

## A layout bug found by the tests

An 80-character title caused a horizontal overflow on a 360px viewport. The [failing CI run](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371460770) measured a page width of 1,455px. The ticket title was not wrapping.

Adding `overflow-wrap: anywhere` to the title fixed the issue. The next [CI run](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371558410) passed the same regression test.

## Seeded failures

`?defect=currency` deliberately renders the wrong currency format in French; `?defect=status-label` deliberately leaves an English label in place. The associated Pytest cases use **strict expected failures**, so the suite checks that these defects are detected instead of silently passing them.

These are examples introduced for testing, not bugs discovered in an external product.

## Reports and evidence

The GitHub Actions workflow runs Chromium tests and uploads `ui-test-evidence`, containing an HTML test report, experiment measurements and screenshots/traces from failures or expected defect detections.

For a failing test, the fixture writes screenshots and Playwright traces under `artifacts/failures/`. Open a trace with `python -m playwright show-trace <path-to-trace.zip>`.

## Repository layout

- `sample_app/` — local ticket-desk app
- `test_support/` — disposable local HTTP server
- `tests/` — Python UI tests and test fixtures
- `scripts/reliability_experiment.py` — measured timing comparison
- `docs/` — architecture and test plan
- `DEVELOPMENT_LOG.md` — decisions, debugging and measured evidence
- `.github/workflows/ui-tests.yml` — CI and artifact upload

## Limits

The project tests a browser app with Chromium, not native iOS/macOS software. The timing delays and two localization defects are controlled examples. The evidence should be interpreted as results from those specific scenarios, not general performance guarantees.
