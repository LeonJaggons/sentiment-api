import re
from datetime import datetime

from fastapi.responses import JSONResponse
from transformers import pipeline

from util.constants import MAX_TEXT_LENGTH, MODEL_NAME
from util.custom_types import SentimentAnalysisResponse

# Sevice functions to handle sentiment analysis business logic

processed_sentiments = []

sentiment_analyzer = pipeline(MODEL_NAME)


def is_invalid_text(text: str | None) -> dict[str, str] | None:
    """
    Validate the text to ensure it is not empty and does not exceed the maximum length
    Args:
        text (str): The text to be validated
    Returns:
        dict[str, str] | None: The error message if the text is invalid, otherwise None
    """

    if not text or text == "":
        return {"status_code": 400, "message": "'text' field is required"}
    if len(text.split(" ")) > MAX_TEXT_LENGTH:
        return {
            "status_code": 422,
            "message": f"'text' is too long. Max length is {MAX_TEXT_LENGTH} words",
        }
    if not re.search(r"[a-zA-Z0-9]", text):
        return {
            "status_code": 422,
            "message": "'text' must contain at least one letter or number",
        }

    return None


def get_text_sentiment(text: str) -> SentimentAnalysisResponse | JSONResponse:
    """
    Validate text, analyze the sentiment and return the result
    Args:
        text (str): The text to be analyzed
    Returns:
        SentimentAnalysisResponse: The sentiment analysis result
    """

    error = is_invalid_text(text)
    if error:
        return JSONResponse(
            status_code=error["status_code"], content={"detail": error["message"]}
        )

    sentiment = sentiment_analyzer(text)
    sentiment_data = sentiment[0]
    created_at = datetime.now()

    analyzed_sentiment: SentimentAnalysisResponse = {
        "text": text,
        "sentiment": sentiment_data["label"],
        "confidence_score": sentiment_data["score"],
        "created_at": created_at,
    }

    write_sentiment(analyzed_sentiment)

    return analyzed_sentiment


def write_sentiment(sentiment: SentimentAnalysisResponse):
    """
    Write the sentiment to the local processed_sentiments list
    Args:
        sentiment (SentimentAnalysisResponse): The sentiment to be written
    """

    processed_sentiments.insert(0, sentiment)


def get_recent_sentiment(limit: int = 5) -> list[SentimentAnalysisResponse]:
    """
    Get the most recent sentiment analysis results
    Args:
        limit (int): The number of recent sentiments to return
    Returns:
        list[SentimentAnalysisResponse]: The list of recent sentiment analysis results
    """

    # Probably redudant since we insert at index 0 in write_sentiment but just to be safe
    sorted_sentiments = sorted(
        processed_sentiments, key=lambda x: x["created_at"], reverse=True
    )
    return sorted_sentiments[:limit]


def clear_recent_sentiment():
    """
    Clear the list of recent sentiment analysis results
    """
    processed_sentiments.clear()
    return JSONResponse(
        status_code=200, content={"message": "Recent sentiments cleared"}
    )
