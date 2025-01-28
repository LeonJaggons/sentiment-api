from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# Strongly typed data models to be used in the sentiment analysis router
# for validating requests, better code transparency and readability


class SentimentAnalysisRequest(BaseModel):
    text: Optional[str]


class InvalidSentimentAnalysisRequest(BaseModel): ...


class SentimentAnalysisResponse(BaseModel):
    text: str
    sentiment: str
    confidence_score: float
    created_at: datetime
