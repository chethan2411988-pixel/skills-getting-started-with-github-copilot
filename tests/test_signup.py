from fastapi.testclient import TestClient
import urllib.parse

from src import app as _app_module

client = TestClient(_app_module.app)


def test_duplicate_signup():
    # create a temporary activity for testing
    name = "Test Activity"
    _app_module.activities[name] = {
        "description": "",
        "schedule": "",
        "max_participants": 2,
        "participants": [],
    }

    email = "alice@example.com"
    url = f"/activities/{urllib.parse.quote(name)}/signup?email={urllib.parse.quote(email)}"

    r1 = client.post(url)
    assert r1.status_code == 200

    r2 = client.post(url)
    assert r2.status_code == 400
    assert "already" in r2.json().get("detail", "").lower()

    # cleanup
    del _app_module.activities[name]


def test_capacity_limit():
    name = "Capacity Activity"
    _app_module.activities[name] = {
        "description": "",
        "schedule": "",
        "max_participants": 1,
        "participants": [],
    }

    a = "a@example.com"
    b = "b@example.com"
    url_a = f"/activities/{urllib.parse.quote(name)}/signup?email={urllib.parse.quote(a)}"
    url_b = f"/activities/{urllib.parse.quote(name)}/signup?email={urllib.parse.quote(b)}"

    ra = client.post(url_a)
    assert ra.status_code == 200

    rb = client.post(url_b)
    assert rb.status_code == 400
    assert "full" in rb.json().get("detail", "").lower()

    del _app_module.activities[name]
