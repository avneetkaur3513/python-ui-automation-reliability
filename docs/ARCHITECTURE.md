# Architecture

This is a Python-driven browser regression testing project. The application under test is a small local ticket desk, so test conditions can be reproduced without relying on a third-party website.

## Components

- `sample_app/`: a local browser application with ordinary user workflows and a language switcher. Its behaviour should be deterministic unless a test explicitly introduces a fault.
- `tests/conftest.py`: starts an HTTP server and provides a clean Playwright browser context for each test.
- `tests/`: Pytest scenarios with observable assertions. Tests should not rely on fixed sleeps or order-dependent state.
- `docs/`: decisions, test cases and investigation evidence.
- GitHub Actions (future stage): runs the tests and retains relevant failure artifacts.

## Test flow

1. Start the local application on an available loopback port.
2. Launch a Chromium browser using Playwright.
3. Execute an isolated user journey with Pytest.
4. Assert on visible content and behaviour, not merely on successful clicks.
5. When a test fails, investigate the browser trace, page state and timing rather than hiding the issue with retries.

## Next engineering problems

1. **Reliability:** reproduce a genuinely intermittent UI timing problem, identify the cause, then measure repeat runs before and after a fix.
2. **Localization:** validate translated interface labels, regional formatting and layout under at least two locales.
3. **Failure diagnosis:** capture useful artifacts and summarize failures without depending on an LLM.

Avoid inventing performance numbers; report actual counts and conditions when these experiments exist.
