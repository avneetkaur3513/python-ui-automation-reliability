# Debugging notes

These notes explain the decisions behind the tests. Each investigation has a failing test, a change, and a passing CI run. Numbers below are from the linked runs, not estimates.

## 1. Keyboard focus after a status change

**Problem:** The ticket list gets rebuilt after resolving or reopening a ticket. The old button is removed, so keyboard focus is lost. A user cannot just press Enter again on that ticket.

**Reproduction:** `tests/test_keyboard_nav.py` focuses a Resolve button, activates it with Enter, then expects the replacement Reopen button to have focus. Two new tests failed in [CI before the fix](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42374596784).

**Change:** Keep track of each ticket's position in the underlying list. After the UI is updated, focus the button for the same ticket. If the active status filter hides it, focus the filter instead. The extra case verifies that focus does not disappear when the row leaves the view.

**Result:** All three keyboard-navigation tests passed in [CI after the fix](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42374826958), together with the existing tests.

Relevant code: `sample_app/index.html`, `tests/test_keyboard_nav.py`.

## 2. A form that accepted blank values

**Problem:** HTML `required` prevents an empty field, but a string of spaces still counts as a value.

**Reproduction:** Three new cases in `tests/test_form_validation.py` submitted a blank title, blank details, and both. All three failed because a new ticket was created. See [CI evidence](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42373751983).

**Change:** Validate trimmed values before creating a ticket. Show an accessible error message and translate it for French. Hide the error once the user edits the field.

**Result:** The validation cases and recovery checks passed in [the subsequent run](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42374057583).

## 3. Fixed sleeps versus waiting for a result

**Problem:** A test that sleeps for an arbitrary duration may pass for a fast response and fail for a slower one.

**Experiment:** `scripts/reliability_experiment.py` deliberately delays search updates by 20 ms or 260 ms. A 100 ms fixed wait succeeded in 6 of 12 trials; waiting for the expected number of rows succeeded in 12 of 12. See [measured CI run](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371084086).

**Choice:** Ordinary UI tests use Playwright assertions that wait for an observable condition. The fixed wait appears only in this comparison script.

**Limit:** The delay was injected. These figures are not a real-world flaky-test rate or a claim that the underlying application is randomly unreliable.

## 4. Narrow-screen title overflow

**Problem:** An 80-character uninterrupted title did not wrap at a 360 px viewport and pushed the document width to 1,455 px.

**Reproduction:** `tests/test_mobile_layout.py` measured the page's available and scroll widths. The [first run failed](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371460770).

**Change:** Apply `overflow-wrap: anywhere` to ticket titles.

**Result:** The test passed in [the next CI run](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42371558410).

## Why two kinds of application?

The small local ticket desk makes it possible to inject controlled errors and reproduce them consistently. The external TodoMVC demo checks whether the Python test setup works against an independently maintained interface.

The external tests run in separate GitHub Actions jobs for Chromium and Firefox. Each test gets a new browser context, preventing the demo's localStorage state from leaking between cases.

## Practical demonstration

Install the dependencies as described in `README.md`, then run:

```bash
python -m pytest -q tests/test_keyboard_nav.py
python -m pytest -q tests/test_form_validation.py
python -m pytest -q -m "not external"
python -m scripts.reliability_experiment --iterations 12
```

To interact with the test application directly:

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory sample_app
```

Open `http://127.0.0.1:8000`, select a language, create a ticket and try Resolve/Reopen using Tab and Enter. The browser tests are the authoritative automated checks; manual interaction is useful for understanding the UI.

## Design choices worth explaining

- **Why Python + Playwright?** Browser automation and its observable assertions are the focus, rather than native-app implementation.
- **Why Pytest fixtures?** A test starts with a clean browser context and the local HTTP server is shared across the session.
- **Why save a trace?** A screenshot shows the final page state, whereas a Playwright trace helps inspect the sequence of actions around failure.
- **Why keep injected defects separate?** The test checks the exact expected broken output and verifies the correct output without injection. This avoids treating any unrelated exception as successful defect detection.
- **What is not covered?** Native iOS/macOS automation, production application defects, and broad performance claims. The external site is a public testing demo.

The tests and results are reproducible evidence, but understanding the code and rerunning the experiments matters more than memorising these notes.
