# Architecture

The system has four small parts:

1. **Ticket-desk web app:** HTML and JavaScript for searching, creating and updating tickets. English/French UI, local date/currency formatting and controlled test-only defects are included.
2. **Local HTTP server:** `test_support/server.py` starts the app on a free loopback port. It is shared between Pytest and the timing experiment.
3. **Playwright + Pytest:** fresh browser contexts, visible assertions and test isolation. When a test fails or detects a seeded defect, the fixture saves a screenshot and Playwright trace.
4. **GitHub Actions:** runs the tests, performs the timing comparison and publishes the HTML report plus artifacts.

## Why the app is local

Testing somebody else's site makes state, language support and timing difficult to control. The local ticket desk provides repeatable conditions so the tests can investigate specific behaviours.

## Reliability investigation

The optional `searchDelay` URL parameter controls asynchronous search updates. The experiment alternates between short and long updates to compare:

- a weak test using a fixed 100 ms delay
- a test waiting for the UI to show the expected result

Normal tests use Playwright's condition-based assertions, not fixed sleeps. The fixed wait exists only in the demonstration script.

## Localization checks

The app uses `Intl.DateTimeFormat` and `Intl.NumberFormat` for `en-IE` and `fr-FR`. Tests verify visible translations, the expected number/date formats, and layout at narrow viewport widths.

Test-only fault switches allow reproducible negative controls without permanently breaking the normal application.

## Limits

This is browser automation, not native app testing. The timed conditions and injected translation errors are reproducible simulations. See `README.md` for evidence links and `DEVELOPMENT_LOG.md` for the measured outcomes.
