# Next steps

Current working branch: `ui-tests` (branched from `feature/01-foundation`).
Do not merge into `main` yet. The earlier branch is still present on GitHub.

## Built so far

- Local ticket-desk app with search, ticket creation and required-field validation.
- English and French UI translations.
- Resolve/reopen ticket actions and status filtering.
- Python Playwright/Pytest smoke and workflow tests.
- GitHub Actions with an HTML report artifact.

## Run locally

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m pytest -q --html=report.html --self-contained-html
```

## Work that remains

1. Confirm the latest GitHub Actions run is successful; investigate any failures.
2. Add and diagnose a controlled intermittent UI timing problem; measure repeated runs.
3. Extend testing for regional formatting or layout differences with real assertions.
4. Preserve screenshots/traces on failure and document reproducible defect examples.
5. Review CI output, README and test evidence before deciding the project is complete.

Do not claim measured improvements until the experiments have actually run.
