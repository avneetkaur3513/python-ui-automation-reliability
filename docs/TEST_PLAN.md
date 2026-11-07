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
