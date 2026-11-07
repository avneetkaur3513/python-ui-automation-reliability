# Project handoff

Current integration branch: `main`. The `test-review` branch contains the latest form-validation and negative-control audit work until its pull request is merged.

## What works

- Python/Playwright/Pytest UI automation against a controlled local ticket app.
- Cross-language labels, date/currency formatting, navigation, forms and ticket status workflows.
- A measured fixed-wait vs state-based wait experiment.
- Detection and fix of a mobile text overflow defect.
- Deliberately injected localization defects with exact-value checks rather than unconditional expected failures.
- Input validation rejects whitespace-only values; error recovery and French error messages are tested.
- Additional external TodoMVC regression tests in Chromium and Firefox.
- GitHub Actions HTML reports, failure screenshots and traces.

## CI and evidence

- Failing form-validation run: https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42373751983
- Passing review run: https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42374057583
- Latest review result: 29 local tests passed, 8 external Chromium passed, 8 external Firefox passed.
- The 12-run timing experiment is deliberately controlled, not a production benchmark.

## Local commands

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m pytest -q -m "not external" --html=report.html --self-contained-html
python -m scripts.reliability_experiment
```

External tests require network access: `python -m pytest -q -m external`. Install Firefox and set `PLAYWRIGHT_BROWSER=firefox` to test that engine.

## Next human review

Check the latest GitHub Actions run, inspect `README.md`, and be able to explain the failure-first investigation for whitespace validation, mobile overflow, and the fixed-wait experiment. These are controlled engineering exercises, not claims about production software or native Apple-platform testing.
