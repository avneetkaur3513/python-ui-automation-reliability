from playwright.sync_api import expect


def test_delayed_search_eventually_updates_results(page, app_url):
    page.goto(f"{app_url}?searchDelay=220")
    page.get_by_label("Search tickets").fill("payment")
    expect(page.get_by_test_id("ticket-item")).to_have_count(1)
    expect(page.get_by_text("Payment page loads slowly")).to_be_visible()


def test_newer_search_replaces_pending_update(page, app_url):
    page.goto(f"{app_url}?searchDelay=250")
    search = page.get_by_label("Search tickets")
    search.fill("login")
    search.fill("payment")
    expect(page.get_by_test_id("ticket-item")).to_have_count(1)
    expect(page.get_by_text("Payment page loads slowly")).to_be_visible()
    expect(page.get_by_text("Login button is unresponsive")).to_have_count(0)


def test_clear_search_recovers_all_rows_after_delay(page, app_url):
    page.goto(f"{app_url}?searchDelay=150")
    search = page.get_by_label("Search tickets")
    search.fill("profile")
    expect(page.get_by_test_id("ticket-item")).to_have_count(1)
    search.clear()
    expect(page.get_by_test_id("ticket-item")).to_have_count(3)
