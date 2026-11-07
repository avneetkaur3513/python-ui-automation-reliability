from playwright.sync_api import expect


def test_long_ticket_title_fits_mobile_screen(page, app_url):
    page.set_viewport_size({"width": 360, "height": 780})
    page.goto(app_url)
    page.get_by_label("Language").select_option("fr")

    title = "W" * 80
    page.locator("#ticket-title").fill(title)
    page.locator("#ticket-details").fill("Reproduction for narrow layouts.")
    page.get_by_role("button", name="Créer un ticket").click()

    expect(page.get_by_text(title, exact=True)).to_be_visible()
    dimensions = page.evaluate("""() => ({
        available: document.documentElement.clientWidth,
        content: document.documentElement.scrollWidth
    })""")
    assert dimensions["content"] <= dimensions["available"], (
        f"Unexpected horizontal overflow on mobile: {dimensions}"
    )
