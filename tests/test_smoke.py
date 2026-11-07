from playwright.sync_api import expect


def test_ticket_list_loads(page, app_url):
    page.goto(app_url)
    expect(page.get_by_role("heading", name="Ticket Desk")).to_be_visible()
    expect(page.get_by_test_id("ticket-item")).to_have_count(3)


def test_language_switch_updates_interface(page, app_url):
    page.goto(app_url)
    page.locator("#locale").select_option("fr")
    expect(page.get_by_role("heading", name="Centre de tickets")).to_be_visible()
    expect(page.locator("#search-label")).to_have_text("Rechercher des tickets")


def test_search_filters_tickets(page, app_url):
    page.goto(app_url)
    page.locator("#search").fill("payment")
    expect(page.get_by_test_id("ticket-item")).to_have_count(1)
    expect(page.get_by_text("Payment page loads slowly")).to_be_visible()


def test_create_ticket_updates_list(page, app_url):
    page.goto(app_url)
    page.locator("#ticket-title").fill("Checkout receipt not shown")
    page.locator("#ticket-details").fill("Receipt is missing after payment.")
    page.get_by_role("button", name="Create ticket").click()
    expect(page.get_by_test_id("ticket-item")).to_have_count(4)
    expect(page.get_by_text("Checkout receipt not shown")).to_be_visible()
