# Test plan

The first milestone validates that the local app and browser-test harness work. Future tests should cover failures that are worth debugging rather than adding assertions just to increase the test count.

| Area | Initial baseline | Future investigation |
| --- | --- | --- |
| Page health | App loads and seeded tickets appear | Meaningful error state when data is unavailable |
| Navigation and input | Search and create a ticket | Validation, keyboard navigation and edge cases |
| Localization | English and French labels | Region-specific formats, long strings, layout defects |
| Reliability | Tests use Playwright's auto-waiting assertions | Controlled async race, reproduced failure and measured fix |
| Reporting | Terminal Pytest output | Screenshots, traces, HTML and CI artifacts |

## Test quality rules

- Prefer user-visible outcomes to private implementation details.
- Each test should be runnable on its own.
- Keep the test app and test framework separate.
- Use deterministic data for baseline runs.
- Deliberately injected bugs must be clearly documented and reverted or isolated.
- Record actual commands, failures and measurements in the development log.

## Additional tested workflows

The `ui-tests` branch adds expected behaviours for:
- Case-insensitive search, clearing search and empty states
- Browser-enforced form validation
- New ticket visibility when a filter was active
- Resolve/reopen actions and status filtering
- French status/action translations
- User-entered text displayed literally, not interpreted as HTML

These are deterministic regression tests. Flaky-test diagnosis and regional format validation are separate future investigations.

## External regression tests

The `external` marker distinguishes external-app tests from the controlled local app. The first target is the official Playwright TodoMVC demo, chosen because it supports reproducible CRUD, browser routing and persistence without registration.

Scenarios:
- Add multiple entries in expected order
- Reject blank/whitespace input
- Show the correct set under Active/Completed filters
- Clear completed items without deleting active items
- Save an edited entry without making a duplicate
- Cancel an edit with Escape
- Retain titles and completion state after reload
- Delete a selected item while leaving unrelated items intact

The external suite runs in separate CI jobs; both Chromium and Firefox are intended. A third-party outage is reported as a test failure rather than masked. This suite does not verify native iOS or macOS behaviour.

## Form-validation and seeded-defect review

- Submit whitespace-only title, whitespace-only details, and both simultaneously; none should create a ticket.
- Correct an invalid title and verify submission succeeds, proving the error state can recover.
- Switch to French and check the invalid-submission message is translated.
- A negative-control test must assert the exact known wrong value under injection and the exact correct behaviour without injection. General `xfail` handling is too permissive because it can hide unrelated exceptions.

The initial whitespace tests failed as intended (CI 42373751983); after the fix and explicit negative controls, all 29 local tests passed (CI 42374057583).
