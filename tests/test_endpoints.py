from fastapi.testclient import TestClient

from main import app
from util.constants import MAX_TEXT_LENGTH

client = TestClient(app=app)


def test_analyze_sentiment():
    text = "this is the best, most amazing pytest test ever written!"
    response = client.post("/sentiment/analyze", json={"text": text})
    assert response.status_code == 201

    # Remove the created_at field from the response for comparison
    result = response.json()
    del result["created_at"]

    assert result == {
        "text": text,
        "sentiment": "POSITIVE",
        "confidence_score": 0.9998314380645752,
    }


def test_analyze_missing_text():
    response = client.post("/sentiment/analyze", json={"text": ""})
    assert response.json() == {"detail": "'text' field is required"}
    assert response.status_code == 400


def test_analyze_long_text():
    response = client.post("/sentiment/analyze", json={"text": "a " * 1001})
    assert response.status_code == 422
    assert response.json() == {
        f"detail": f"'text' is too long. Max length is {MAX_TEXT_LENGTH} words"
    }


def test_analyze_nonalha_text():
    response = client.post("/sentiment/analyze", json={"text": "😂"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": "'text' must contain at least one letter or number"
    }


def test_get_write_sentiment():
    text = "written test to test the write_sentiment function"
    response = client.post("/sentiment/analyze", json={"text": text})
    assert response.status_code == 201

    response = client.get("/sentiment/recent")
    assert response.status_code == 200

    assert type(response.json()) == list
    result = response.json()[0]

    assert result["text"] == text
    del result["created_at"]

    assert result == {
        "text": text,
        "sentiment": "NEGATIVE",
        "confidence_score": 0.9960417747497559,
    }


def test_not_write_with_missing_text():
    response = client.post("/sentiment/analyze", json={"text": ""})
    assert response.status_code == 400

    response = client.get("/sentiment/recent?limit=0")
    assert response.status_code == 200

    assert response.json() == []


def test_no_write_with_long_text():
    response = client.post("/sentiment/analyze", json={"text": "a " * 3001})
    assert response.status_code == 422

    response = client.get("/sentiment/recent?limit=0")
    assert response.status_code == 200

    assert response.json() == []


def test_no_write_with_nonalpha_text():
    response = client.post("/sentiment/analyze", json={"text": "😂"})
    assert response.status_code == 422

    response = client.get("/sentiment/recent?limit=0")
    assert response.status_code == 200

    assert response.json() == []


def test_default_five_items_in_recent():
    for i in range(5):
        response = client.post("/sentiment/analyze", json={"text": f"test {i}"})
        assert response.status_code == 201

    response = client.get("/sentiment/recent")
    assert response.status_code == 200

    assert len(response.json()) == 5
