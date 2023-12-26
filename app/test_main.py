import pytest
from fastapi.testclient import TestClient
from main import app
from mongomock import MongoClient

app.mongodb = MongoClient()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    "word_data, expected_status, expected_word",
    [
        ({"word": "apple"}, 201, "apple"),
        ({"word": "apple"}, 200, "apple"),
    ],
)
def test_add_word(client, word_data, expected_status, expected_word):
    # Setup
    if expected_status == 201:
        client.delete(f"/word/{word_data['word']}")

    response = client.post("/word", json=word_data)
    assert response.status_code == expected_status
    assert "word" in response.json()
    assert response.json()["word"] == expected_word


def test_get_word_list(client):
    response = client.get("/words")
    assert response.status_code == 200
    assert "total" in response.json()
    assert "items" in response.json()


@pytest.mark.parametrize(
    "word_to_delete, expected_status",
    [
        ("delete_me", 200),
        ("nonexistent_word", 404),
    ],
)
def test_delete_word(client, word_to_delete, expected_status):
    # Setup
    if expected_status == 200:
        client.post("/word", json={"word": word_to_delete})
    else:
        client.delete(f"/word/{word_to_delete}")

    response = client.delete(f"/word/{word_to_delete}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert "message" in response.json()
        assert response.json()["message"] == "Word deleted successfully"
