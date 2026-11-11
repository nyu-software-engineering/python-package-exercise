from html.parser import HTMLParser

import pytest

from app import create_app


class PageElements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


@pytest.fixture
def client(tmp_path):
    app = create_app(tmp_path / "quests.db")
    app.config["TESTING"] = True
    return app.test_client()


def test_home_has_saved_quest_controls_and_existing_creation_form(client):
    response = client.get("/")
    assert response.status_code == 200
    page = PageElements()
    page.feed(response.get_data(as_text=True))
    ids = [attrs["id"] for _, attrs in page.elements if "id" in attrs]
    assert len(ids) == len(set(ids))
    assert {"quest-form", "quest-list", "quest-filter", "quest-detail", "progress-summary", "refresh-quests"} <= set(ids)
    assert sum(tag == "main" for tag, _ in page.elements) == 1
    assert sum(tag == "h1" for tag, _ in page.elements) == 1
    assert ("html", {"lang": "en"}) in page.elements
    assert any(tag == "meta" and attrs.get("name") == "viewport" for tag, attrs in page.elements)


def test_wrapper_keeps_a_working_creation_token(client):
    page = PageElements()
    page.feed(client.get("/").get_data(as_text=True))
    form = next(attrs for tag, attrs in page.elements if attrs.get("id") == "quest-form")
    assert form["data-csrf-token"]
    response = client.post(
        "/quests", json={"title": "Study math", "durationMinutes": 30},
        headers={"X-CSRF-Token": form["data-csrf-token"]},
    )
    assert response.status_code == 201
    assert client.get("/quests").get_json() == [response.get_json()]


@pytest.mark.parametrize("path, content_type", [("/static/quest_form.js", "javascript"), ("/static/quest_list.js", "javascript"), ("/static/planner.css", "text/css")])
def test_page_assets_are_served(client, path, content_type):
    response = client.get(path)
    assert response.status_code == 200
    assert content_type in response.content_type


def test_home_contains_no_inline_scripts(client):
    page = PageElements()
    page.feed(client.get("/").get_data(as_text=True))
    scripts = [attrs for tag, attrs in page.elements if tag == "script"]
    assert {attrs["src"] for attrs in scripts} == {"/static/quest_form.js", "/static/quest_list.js"}
    assert not any(name.startswith("on") for _, attrs in page.elements for name in attrs)
