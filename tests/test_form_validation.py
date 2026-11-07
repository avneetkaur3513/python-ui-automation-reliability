"""Form validation cases that should not create blank tickets."""

import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize(
    "title,details",
    [
        ("   ", "The title is only whitespace."),
        ("Useful title", "   "),
        ("\t  ", " \t "),
    ],
)
def test_whitespace_only_fields_do_not_create_ticket(page, app_url, title, details):
    page.goto(app_url)
    page.locator("#ticket-title").fill(title)
    page.locator("#ticket-details").fill(details)

    page.get_by_role("button", name="Create ticket").click()

    expect(page.get_by_test_id("ticket-item")).to_have_count(3)
    expect(page.locator("#ticket-count")).to_have_text("3 tickets")
