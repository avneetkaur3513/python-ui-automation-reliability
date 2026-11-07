from playwright.sync_api import expect


def test_search_matches_title_without_case_sensitivity(page, app_url):
    page.goto(app_url)
    page.get_by_label("Search tickets").fill("PAYMENT")
    expect(page.get_by_test_id("ticket-item")).to_have_count(1)
    expect(page.get_by_text("Payment page loads slowly")).to_be_visible()


def test_search_can_be_cleared(page, app_url):
    page.goto(app_url)
    search = page.get_by_label("Search tickets")
    search.fill("login")
    expect(page.get_by_test_id("ticket-item")).to_have_count(1)
    search.clear()
    expect(page.get_by_test_id("ticket-item")).to_have_count(3)


def test_unmatched_search_shows_empty_state(page, app_url):
    page.goto(app_url)
    page.get_by_label("Search tickets").fill("does-not-exist")
    expect(page.get_by_text("No tickets found")).to_be_visible()
    expect(page.get_by_test_id("ticket-item")).to_have_count(0)


def test_empty_state_is_translated(page, app_url):
    page.goto(app_url)
    page.get_by_label("Language").select_option("fr")
    page.get_by_label("Rechercher des tickets").fill("unknown")
    expect(page.get_by_text("Aucun ticket trouvé")).to_be_visible()
    expect(page.locator("html")).to_have_attribute("lang", "fr")


def test_ticket_title_is_required(page, app_url):
    page.goto(app_url)
    page.get_by_label("Details").fill("Some details")
    page.get_by_role("button", name="Create ticket").click()
    expect(page.get_by_test_id("ticket-item")).to_have_count(3)
    expect(page.locator("#ticket-title")).to_have_attribute("required", "")


def test_ticket_details_are_required(page, app_url):
    page.goto(app_url)
    page.get_by_label("Title").fill("Missing details")
    page.get_by_role("button", name="Create ticket").click()
    expect(page.get_by_test_id("ticket-item")).to_have_count(3)
    expect(page.locator("#ticket-details")).to_have_attribute("required", "")


def test_creation_resets_filters_so_new_ticket_is_visible(page, app_url):
    page.goto(app_url)
    page.get_by_label("Search tickets").fill("login")
    page.get_by_label("Status").select_option("resolved")
    page.get_by_label("Title").fill("Cannot export tickets")
    page.get_by_label("Details").fill("Export button does not respond.")
    page.get_by_role("button", name="Create ticket").click()
    expect(page.get_by_label("Search tickets")).to_have_value("")
    expect(page.get_by_label("Status")).to_have_value("all")
    expect(page.get_by_test_id("ticket-item")).to_have_count(4)
    expect(page.get_by_text("Cannot export tickets")).to_be_visible()


def test_resolving_ticket_moves_it_to_resolved_filter(page, app_url):
    page.goto(app_url)
    page.get_by_role("button", name="Resolve: Payment page loads slowly").click()
    page.get_by_label("Status").select_option("resolved")
    expect(page.get_by_test_id("ticket-item")).to_have_count(1)
    ticket = page.get_by_test_id("ticket-item").first
    expect(ticket).to_contain_text("Payment page loads slowly")
    expect(ticket.locator("span")).to_have_text("Resolved")


def test_resolved_ticket_can_be_reopened(page, app_url):
    page.goto(app_url)
    page.get_by_role("button", name="Resolve: Payment page loads slowly").click()
    page.get_by_label("Status").select_option("resolved")
    page.get_by_role("button", name="Reopen: Payment page loads slowly").click()
    expect(page.get_by_test_id("ticket-item")).to_have_count(0)
    page.get_by_label("Status").select_option("open")
    expect(page.get_by_test_id("ticket-item")).to_have_count(3)


def test_status_actions_are_translated_to_french(page, app_url):
    page.goto(app_url)
    page.get_by_label("Language").select_option("fr")
    expect(page.get_by_label("Statut")).to_be_visible()
    page.get_by_role("button", name="Résoudre: Login button is unresponsive").click()
    page.get_by_label("Statut").select_option("resolved")
    ticket = page.get_by_test_id("ticket-item").first
    expect(ticket.locator("span")).to_have_text("Résolu")
    expect(page.get_by_role("button", name="Rouvrir: Login button is unresponsive")).to_be_visible()


def test_user_text_is_displayed_as_text_not_html(page, app_url):
    page.goto(app_url)
    title = '<img src="bad" onerror="alert(1)">'
    page.get_by_label("Title").fill(title)
    page.get_by_label("Details").fill("Plain text only.")
    page.get_by_role("button", name="Create ticket").click()
    expect(page.get_by_text(title, exact=True)).to_be_visible()
    expect(page.locator("img")).to_have_count(0)
