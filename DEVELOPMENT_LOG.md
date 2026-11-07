# Development log

## 2026-11-07 — Foundation

- Created `feature/01-foundation` from initial `main` commit.
- Documented architecture, test strategy and intended engineering investigations.
- Added a deterministic local ticket desk with English/French UI, search and ticket creation.
- Added Python Playwright/Pytest fixtures and four smoke scenarios.
- Added GitHub Actions workflow to run Chromium tests and upload HTML results.

### Verification performed

- Python files: `python -m py_compile` passed.
- Inline application JavaScript: `node --check` passed.
- Local Playwright run: 4 tests blocked at browser navigation by this sandbox's `ERR_BLOCKED_BY_ADMINISTRATOR`. This is **not** evidence that they pass in a normal browser or CI.
- GitHub Actions CI: status must be checked independently. Do not report tests as passing until a completed run confirms it.

### Foundation commits

- `a1b26c3` — architecture and test plan
- `a27c24b` — demo application
- `f187258` — initial Python smoke tests
- `9cc21f3` — GitHub Actions workflow

The repository is not yet a complete automation/reliability portfolio project.

## 2026-11-07 — UI workflows

- Created the shorter working branch `ui-tests` with existing commits preserved.
- Added ability to resolve and reopen tickets with filtered open/resolved views.
- Added English and French status/action labels, including accessible button names.
- Added 11 Playwright tests covering search, form validation, status changes, translations and safe text rendering.
- Changes committed separately as app functionality and test coverage.
- GitHub Actions confirmed **15 tests passed** on commit `d21bde6` (run `42369646052`, 2026-11-07).

## 2026-11-07 — Reliability and localization

- Added a test-only asynchronous search delay and three Playwright tests for late updates.
- Moved the local HTTP server into a shared helper for tests and investigation scripts.
- Added a timing experiment comparing a fixed wait with a condition-based assertion.
- Added automatic screenshots and Playwright traces for failures and expected defect detections.
- Added regional date/currency formatting for Ireland and France, plus two strict expected-failure tests for deliberately seeded localization defects.
- Investigated long title overflow on a narrow French mobile layout.

### Verified results

- CI run [42371084086](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371084086): 18 browser tests passed. Controlled timing comparison: fixed wait 6/12; condition-based wait 12/12.
- CI run [42371256205](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371256205): 21 passed and 2 strict expected failures for injected localization defects.
- CI run [42371460770](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371460770) **failed** the newly introduced narrow-screen regression test. At 360px viewport width, the page's scroll width was 1455px.
- Applied `overflow-wrap: anywhere` to the ticket heading, preserving its content while allowing it to wrap.
- CI run [42371558410](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371558410): **22 passed, 2 xfailed**. Timing comparison again: fixed 6/12; condition-based 12/12.

The two xfails are deliberate negative controls, not unresolved failures in the normal app. Timing metrics are measured only under injected test delays.

## 2026-11-07 — Independent site regression coverage

- Added eight Playwright scenarios against the external Playwright TodoMVC demo.
- Scenarios verify item ordering, whitespace validation, filtering, completion, editing, edit cancellation, reload persistence and targeted deletion.
- Separated these tests from the local ticket-desk suite using a Pytest marker.
- GitHub Actions run [42373046982](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42373046982): external job **8 passed**; local job **22 passed, 2 xfailed**.
- Added a Chromium/Firefox matrix for external tests. Cross-browser results must be checked in a later CI run before claiming Firefox coverage has passed.

The demo is a publicly available test application; these tests do not constitute production system validation.
