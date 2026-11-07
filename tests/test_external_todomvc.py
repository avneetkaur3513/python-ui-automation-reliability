"""Regression checks against an independently maintained browser application.

The official Playwright TodoMVC demo is intentionally used here as an external
application under test. Each test gets a fresh browser context, so the demo's
localStorage data does not leak between tests.

These tests need internet access and are kept separate from the local suite.
"""

import pytest
from playwright.sync_api import expect


DEMO_URL = "https://demo.playwright.dev/todomvc/"


@pytest.fixture
def todo_page(page):
    page.goto(DEMO_URL, wait_until="domcontentloaded", timeout=30000)
    expect(page.locator(".new-todo")).to_be_visible()
    return page


def add_todo(page, title):
    entry = page.locator(".new-todo")
    entry.fill(title)
    entry.press("Enter")


@pytest.mark.external
def test_multiple_items_keep_their_order(todo_page):
    titles = ["Prepare test data", "Investigate failing journey", "Record findings"]
    for title in titles:
        add_todo(todo_page, title)

    expect(todo_page.locator(".todo-list li")).to_have_count(3)
    expect(todo_page.locator(".todo-list li label")).to_have_text(titles)


@pytest.mark.external
def test_blank_entries_are_not_added(todo_page):
    add_todo(todo_page, "   ")
    expect(todo_page.locator(".todo-list li")).to_have_count(0)

    add_todo(todo_page, "  Check empty submissions  ")
    expect(todo_page.locator(".todo-list li label")).to_have_text(
        ["Check empty submissions"]
    )


@pytest.mark.external
def test_active_and_completed_filters_show_correct_items(todo_page):
    add_todo(todo_page, "Fix asynchronous issue")
    add_todo(todo_page, "Review translations")

    todo_page.locator(".todo-list li").first.locator(".toggle").check()
    todo_page.locator(".filters a[href='#/active']").click()

    expect(todo_page.locator(".todo-list li:visible")).to_have_count(1)
    expect(todo_page.locator(".todo-list li:visible label")).to_have_text(
        ["Review translations"]
    )

    todo_page.locator(".filters a[href='#/completed']").click()
    expect(todo_page.locator(".todo-list li:visible label")).to_have_text(
        ["Fix asynchronous issue"]
    )


@pytest.mark.external
def test_clear_completed_does_not_remove_active_item(todo_page):
    add_todo(todo_page, "Archive completed item")
    add_todo(todo_page, "Keep active item")

    todo_page.locator(".todo-list li").first.locator(".toggle").check()
    todo_page.locator(".clear-completed").click()

    expect(todo_page.locator(".todo-list li label")).to_have_text(
        ["Keep active item"]
    )


@pytest.mark.external
def test_editing_updates_the_item_without_creating_another(todo_page):
    add_todo(todo_page, "Old description")
    todo = todo_page.locator(".todo-list li")
    todo.locator("label").dblclick()
    editor = todo.locator(".edit")
    expect(editor).to_be_visible()
    editor.fill("Updated description")
    editor.press("Enter")

    expect(todo_page.locator(".todo-list li")).to_have_count(1)
    expect(todo_page.locator(".todo-list li label")).to_have_text(
        ["Updated description"]
    )


@pytest.mark.external
def test_escape_cancels_an_ongoing_edit(todo_page):
    add_todo(todo_page, "Keep original title")
    todo = todo_page.locator(".todo-list li")
    todo.locator("label").dblclick()
    editor = todo.locator(".edit")
    editor.fill("This change should be cancelled")
    editor.press("Escape")

    expect(todo_page.locator(".todo-list li label")).to_have_text(
        ["Keep original title"]
    )


@pytest.mark.external
def test_items_and_completion_state_survive_reload(todo_page):
    add_todo(todo_page, "Preserve state")
    add_todo(todo_page, "Remain active")
    todo_page.locator(".todo-list li").first.locator(".toggle").check()

    todo_page.reload()
    expect(todo_page.locator(".todo-list li label")).to_have_text(
        ["Preserve state", "Remain active"]
    )
    expect(
        todo_page.locator(".todo-list li").first.locator(".toggle")
    ).to_be_checked()
    expect(
        todo_page.locator(".todo-list li").nth(1).locator(".toggle")
    ).not_to_be_checked()


@pytest.mark.external
def test_delete_removes_only_the_selected_item(todo_page):
    add_todo(todo_page, "Delete this")
    add_todo(todo_page, "Keep this")
    first = todo_page.locator(".todo-list li").first

    first.hover()
    first.locator(".destroy").click()

    expect(todo_page.locator(".todo-list li label")).to_have_text(
        ["Keep this"]
    )
