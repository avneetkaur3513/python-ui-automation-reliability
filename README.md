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

The baseline suite starts a local HTTP server, launches Chromium headlessly and checks ticket loading, language switching, search and ticket creation. No deployed site is needed.

## Project structure

- `sample_app/` — controlled app for reproducible UI testing
- `tests/` — isolated Pytest + Playwright scenarios
- `docs/ARCHITECTURE.md` — system design and test flow
- `docs/TEST_PLAN.md` — baseline tests and proposed investigations
- `DEVELOPMENT_LOG.md` — progress and verification evidence
- `HANDOFF.md` — checkpoint for subsequent development
- `.github/workflows/ui-tests.yml` — CI smoke tests and HTML report artifact

## Planned work

Expand meaningful user journeys, investigate intermittent failures, validate localization and regional formatting, and capture useful failure evidence. Only report measured results.
