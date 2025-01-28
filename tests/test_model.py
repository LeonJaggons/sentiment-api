import json

from fastapi.testclient import TestClient

import services.sentiment as sentiment_service
from main import app
from util.constants import MAX_TEXT_LENGTH

client = TestClient(app=app)


def test_is_model_loaded():
    assert sentiment_service.sentiment_analyzer is not None


def test_analyze_sentiment():
    text = "this is the best, most amazing pytest test ever written!"

    # Remove the created_at field from the response for comparison
    result = sentiment_service.get_text_sentiment(text)
    del result["created_at"]

    assert result == {
        "text": text,
        "sentiment": "POSITIVE",
        "confidence_score": 0.9998314380645752,
    }


def test_analyze_missing_text():
    text = ""
    error = sentiment_service.get_text_sentiment(text)
    assert error.status_code == 400

    error_json = json.loads(error.body.decode("utf-8"))
    assert error_json == {"detail": "'text' field is required"}


def test_analyze_long_text():
    text = "a " * 1001
    error = sentiment_service.get_text_sentiment(text)
    assert error.status_code == 422

    error_json = json.loads(error.body.decode("utf-8"))
    assert error_json == {
        f"detail": f"'text' is too long. Max length is {MAX_TEXT_LENGTH} words"
    }


def test_analyze_nonalha_text():
    text = "🥶"
    error = sentiment_service.get_text_sentiment(text)
    assert error.status_code == 422

    error_json = json.loads(error.body.decode("utf-8"))
    assert error_json == {"detail": "'text' must contain at least one letter or number"}


def test_get_write_sentiment():
    text = "written test to test the write_sentiment function"

    sentiment_service.get_text_sentiment(text)

    proceesed_sentiments = sentiment_service.processed_sentiments

    assert type(proceesed_sentiments) == list
    result = proceesed_sentiments[0]

    assert result["text"] == text
    del result["created_at"]

    assert result == {
        "text": text,
        "sentiment": "NEGATIVE",
        "confidence_score": 0.9960417747497559,
    }


def test_no_write_with_missing_text():
    sentiment_service.clear_recent_sentiment()

    sentiment_service.get_text_sentiment("")

    response = client.get("/sentiment/recent?limit=0")
    assert response.status_code == 200

    assert response.json() == []


def test_no_write_with_long_text():
    client.post("/sentiment/recent/clear")
    response = client.post("/sentiment/analyze", json={"text": "a " * 3001})
    assert response.status_code == 422

    response = client.get("/sentiment/recent?limit=5")
    assert response.status_code == 200

    assert response.json() == []


def test_no_write_with_nonalpha_text():
    client.post("/sentiment/recent/clear")
    response = client.post("/sentiment/analyze", json={"text": "😂"})
    assert response.status_code == 422

    response = client.get("/sentiment/recent?limit=5")
    assert response.status_code == 200

    assert response.json() == []


def test_default_five_items_in_recent():
    client.post("/sentiment/recent/clear")
    for i in range(5):
        response = client.post("/sentiment/analyze", json={"text": f"test {i}"})
        assert response.status_code == 201

    response = client.get("/sentiment/recent")
    assert response.status_code == 200

    assert len(response.json()) == 5


def test_clear_recent():
    client.post("/sentiment/recent/clear")
    for i in range(5):
        response = client.post("/sentiment/analyze", json={"text": f"test {i}"})
        assert response.status_code == 201

    response = client.get("/sentiment/recent")
    assert response.status_code == 200

    assert len(response.json()) == 5

    response = client.post("/sentiment/recent/clear")
    assert response.status_code == 200

    response = client.get("/sentiment/recent")
    assert response.status_code == 200

    assert response.json() == []


def test_limit_recent():
    client.post("/sentiment/recent/clear")
    for i in range(5):
        response = client.post("/sentiment/analyze", json={"text": f"test {i}"})
        assert response.status_code == 201

    response = client.get("/sentiment/recent?limit=2")
    assert response.status_code == 200

    assert len(response.json()) == 2


def test_recents_is_most_recent():
    client.post("/sentiment/recent/clear")
    for i in range(5):
        response = client.post("/sentiment/analyze", json={"text": f"test {i}"})
        assert response.status_code == 201

    response = client.get("/sentiment/recent")
    assert response.status_code == 200

    assert response.json()[0]["text"] == "test 4"
    assert response.json()[4]["text"] == "test 0"
