from fastapi import APIRouter
from fastapi.responses import JSONResponse

import services.sentiment as sentiment_service
from util.constants import MAX_TEXT_LENGTH
from util.custom_types import (
    InvalidSentimentAnalysisRequest,
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
)

router = APIRouter()

# Endpoints simply invoke the sentiment service functions to separate business logic from the API layer


@router.post("/analyze", status_code=201)
def analyze_sentiment(
    request: SentimentAnalysisRequest | InvalidSentimentAnalysisRequest,
) -> SentimentAnalysisResponse:
    return sentiment_service.get_text_sentiment(request.text)


@router.get("/recent", status_code=200)
def get_recent_sentiment(limit: int = 5) -> list[SentimentAnalysisResponse]:
    return sentiment_service.get_recent_sentiment(limit)


@router.post("/recent/clear", status_code=200)
def clear_recent_sentiment() -> JSONResponse:
    return sentiment_service.clear_recent_sentiment()
