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



def test_form_recovery_after_whitespace_error(page, app_url):
    page.goto(app_url)
    title = page.get_by_label("Title")
    title.fill("   ")
    page.get_by_label("Details").fill("A useful description")
    page.get_by_role("button", name="Create ticket").click()
    expect(page.get_by_role("alert")).to_have_text(
        "Title and details cannot be blank."
    )

    title.fill("Fixed title")
    expect(page.get_by_role("alert")).to_be_hidden()
    page.get_by_role("button", name="Create ticket").click()
    expect(page.get_by_text("Fixed title", exact=True)).to_be_visible()
    expect(page.get_by_test_id("ticket-item")).to_have_count(4)


def test_french_whitespace_error_message(page, app_url):
    page.goto(app_url)
    page.get_by_label("Language").select_option("fr")
    page.get_by_label("Titre").fill("   ")
    page.get_by_label("Détails").fill("Une description")
    page.get_by_role("button", name="Créer un ticket").click()
    expect(page.get_by_role("alert")).to_have_text(
        "Le titre et les détails ne peuvent pas être vides."
    )
