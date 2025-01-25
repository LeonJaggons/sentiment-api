from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers import sentiment

app = FastAPI()

app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])


# Redirect to sentiment router endpoints for better organization and capability to add more endpoints
@app.post("/analyze")
def redirect_analyze():
    return RedirectResponse(url="/sentiment/analyze", status_code=308)


@app.get("/recent")
def redirect_recent():
    return RedirectResponse(url="/sentiment/recent", status_code=308)
