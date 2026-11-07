"""Keyboard behaviour matters when an action replaces its own button."""

from playwright.sync_api import expect


def test_ticket_action_keeps_focus_after_keyboard_activation(page, app_url):
    page.goto(app_url)
    resolve_button = page.get_by_role(
        "button", name="Resolve: Login button is unresponsive"
    )
    resolve_button.focus()
    expect(resolve_button).to_be_focused()

    page.keyboard.press("Enter")

    reopen_button = page.get_by_role(
        "button", name="Reopen: Login button is unresponsive"
    )
    expect(reopen_button).to_be_visible()
    expect(reopen_button).to_be_focused()


def test_keyboard_user_can_toggle_the_same_ticket_twice(page, app_url):
    page.goto(app_url)
    resolve_button = page.get_by_role(
        "button", name="Resolve: Payment page loads slowly"
    )
    resolve_button.focus()
    page.keyboard.press("Enter")
    expect(
        page.get_by_role("button", name="Reopen: Payment page loads slowly")
    ).to_be_focused()

    # The second action should not require starting keyboard navigation over.
    page.keyboard.press("Enter")
    expect(
        page.get_by_role("button", name="Resolve: Payment page loads slowly")
    ).to_be_focused()
