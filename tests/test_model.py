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


def test_analyze_nonalpha_text():
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
    text = "a " * 3500
    sentiment_service.clear_recent_sentiment()

    sentiment_service.get_text_sentiment(text)
    recents = sentiment_service.get_recent_sentiment()

    assert len(recents) == 0


def test_no_write_with_nonalpha_text():
    text = "😂"

    sentiment_service.clear_recent_sentiment()

    sentiment_service.get_text_sentiment(text)
    recents = sentiment_service.get_recent_sentiment()

    assert len(recents) == 0


def test_clear_recent():
    sentiment_service.clear_recent_sentiment()
    limit = 5
    for i in range(limit):
        sentiment_service.get_text_sentiment(f"test {i}")

    recents = sentiment_service.get_recent_sentiment(limit)
    assert len(recents) == limit

    sentiment_service.clear_recent_sentiment()
    cleared_recents = sentiment_service.get_recent_sentiment(limit)
    assert len(cleared_recents) == 0


def test_limit_recent():
    limit = 10
    sentiment_service.clear_recent_sentiment()
    for i in range(limit):
        sentiment_service.get_text_sentiment(f"test {i}")

    recents = sentiment_service.get_recent_sentiment(limit)

    assert len(recents) == limit


def test_recents_is_most_recent():
    sentiment_service.clear_recent_sentiment()
    for i in range(5):
        sentiment_service.get_text_sentiment(f"test {i}")

    recents = sentiment_service.get_recent_sentiment(5)

    assert recents[0]["text"] == "test 4"
    assert recents[4]["text"] == "test 0"
