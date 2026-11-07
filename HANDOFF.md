# Current project status

Working branch: `ui-tests`. The default `main` branch has not been merged or changed.

## Implemented

- Local ticket desk and isolated Pytest + Playwright browser tests.
- Search, create, resolve/reopen, validation and empty-state workflows.
- English/French UI, Irish/French dates and currency, mobile layout regression test.
- Controlled async-search experiment comparing fixed and condition-based waits.
- Reproducible seeded localization defects using strict expected-failure tests.
- Failure screenshots and browser traces, HTML reports and GitHub Actions artifacts.

## Verified

CI run `42371558410`: **22 passed, 2 xfailed**. Reliability script: **6/12 fixed wait** vs **12/12 condition-based**.

A mobile width bug was reproduced in failing CI run `42371460770` and fixed in `eda4f31`. See `DEVELOPMENT_LOG.md`.

## Reproduce locally

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m pytest -q --html=report.html --self-contained-html
python -m scripts.reliability_experiment
```

## Possible next steps

1. Review latest CI run and download its HTML report and traces for a manual inspection.
2. Review code and understand both the timing investigation and mobile overflow fix.
3. Optionally extend with additional browsers or a third locale; neither is necessary to prove the current testing concepts.
4. Merge into `main` only after the project is accepted as ready.

Do not call seeded failures production bugs or timing experiments real-world reliability benchmarks.

## Independent external application tests

A separate `site-regression` branch includes `tests/test_external_todomvc.py` and a new GitHub Actions job for those tests.

Run them with `python -m pytest -q -m external`. The default local suite runs with `-m "not external"`. The external tests use independent browser contexts and require network access.

First external test run: [42373046982](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42373046982), **8 passed**. Chromium/Firefox matrix validated in [run 42373185490](https://github.com/avneetkaur3513/python-ui-automation-reliability/actions/runs/42373185490): 8/8 passed in each browser; local suite also passed.
