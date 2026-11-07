import re

import pytest
from playwright.sync_api import expect


def test_irish_currency_and_date_are_displayed(page, app_url):
    page.goto(app_url)
    expect(page.locator("#example-amount")).to_have_text("€1,234.50")
    expect(page.locator("#example-date")).to_have_text("7 November 2026")


def test_french_currency_and_date_are_displayed(page, app_url):
    page.goto(app_url)
    page.get_by_label("Language").select_option("fr")
    expect(page.locator("#example-date")).to_have_text("7 novembre 2026")
    expect(page.locator("#example-amount")).to_have_text(
        re.compile(r"1\s234,50\s€")
    )
    expect(page.locator("#amount-label")).to_have_text("Montant")


def test_switching_languages_restores_irish_formatting(page, app_url):
    page.goto(app_url)
    page.get_by_label("Language").select_option("fr")
    expect(page.locator("#example-amount")).to_have_text(
        re.compile(r"1\s234,50\s€")
    )
    page.get_by_label("Langue").select_option("en")
    expect(page.locator("#example-amount")).to_have_text("€1,234.50")


@pytest.mark.negative_control
def test_seeded_wrong_currency_is_detected(page, app_url):
    # Assert the actual defective output, not merely that any assertion fails.
    page.goto(f"{app_url}?defect=currency")
    page.get_by_label("Language").select_option("fr")
    expect(page.locator("#example-amount")).to_have_text("€1,234.50")

    # With the injection off, the same French workflow must display the
    # correct locale-specific format.
    page.goto(app_url)
    page.get_by_label("Language").select_option("fr")
    expect(page.locator("#example-amount")).to_have_text(
        re.compile(r"1\\s234,50\\s€")
    )


@pytest.mark.negative_control
def test_seeded_untranslated_status_is_detected(page, app_url):
    page.goto(f"{app_url}?defect=status-label")
    page.get_by_label("Language").select_option("fr")
    expect(page.locator("#status-label")).to_have_text("Status")

    page.goto(app_url)
    page.get_by_label("Language").select_option("fr")
    expect(page.locator("#status-label")).to_have_text("Statut")
