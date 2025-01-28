from fastapi.testclient import TestClient

from main import app
from util.constants import MAX_TEXT_LENGTH

client = TestClient(app=app)


def test_analyze_endpoint():
    client.post("/sentiment/recent/clear")
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


def test_recent_endpoint():
    client.post("/sentiment/recent/clear")
    response = client.get("/sentiment/recent")
    assert response.status_code == 200
    assert response.json() == []


def test_clear_recent_endpoint():
    response = client.post("/sentiment/recent/clear")
    assert response.status_code == 200
