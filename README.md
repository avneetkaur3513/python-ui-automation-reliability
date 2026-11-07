# Python UI Automation & Reliability Framework

A Python and Playwright project exploring how to make UI regression tests reliable, debuggable and useful across languages. A small local ticket-desk app provides reproducible workflows for test experiments.

## Getting started

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Activate .venv: source .venv/bin/activate (macOS/Linux)
# or .venv\Scripts\Activate.ps1 (Windows PowerShell)
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m pytest -q
```

The test suite starts a local HTTP server, launches Chromium headlessly and checks searching, ticket creation, status changes, required fields and English/French translations. No deployed site is needed.

## Project structure

- `sample_app/` — controlled app for reproducible UI testing
- `tests/` — isolated Pytest + Playwright scenarios
- `docs/ARCHITECTURE.md` — system design and test flow
- `docs/TEST_PLAN.md` — baseline tests and proposed investigations
- `DEVELOPMENT_LOG.md` — progress and verification evidence
- `HANDOFF.md` — checkpoint for subsequent development
- `.github/workflows/ui-tests.yml` — CI smoke tests and HTML report artifact

## Planned work

Investigate intermittent failures, test region-sensitive formatting and capture useful failure evidence. The ticket desk is a controlled test fixture rather than a production app. Only report measured results.
