# Take Home Readme

# Sentiment Analysis API

This is a FastAPI-based web service that provides sentiment analysis on input text using a machine learning model from Hugging Face. It also supports database storage of analyzed sentiments and maintains a record with timestamps.

---

## Inital set-up

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

## Running the API

Note: The `/analyze` endpoint will redirect to `/sentiment/analyze`, and `/recent` will redirect to `/sentiment/recent`. FastAPI handles this for you, so you don’t need to worry about the exact path.

### 1. Start the API server

```bash
uvicorn main:app --reload
```

### 2. View Swagger docs to explore available endpoints

```
http://127.0.0.1:8000/docs
```

Note: http://127.0.0.1:8000 is the default domain and port used in many circumstances. Find the url being used after running the API by looking for the terminal line reading: **Uvicorn running on http://x.x.x.x:PORT**

### 3. Make a API request with curl or Swagger

You can make API requests using curl directly from the command line. Here’s how to analyze sentiment using the POST method:

### Example 1: Analyze Sentiment with cURL

Make a POST request to analyze the sentiment of a piece of text:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/sentiment/analyze' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "I absolutely love this API, it's amazing!"
}'
```

### Example 2: Get last 5 Sentiment Records with cURL

```bash
curl -X 'GET' 'http://127.0.0.1:8000/sentiment'
```

## Using Swagger UI

FastAPI provides an interactive web-based interface to test API endpoints through Swagger UI. Here’s how to use it:

### 1. Start the API server if it’s not running yet:

```bash
uvicorn main:app --reload
```

### Access Swagger UI: Open your web browser and go to the following URL:

```text
http://127.0.0.1:8000/docs
```

### Analyze Sentiment:

-   In the Swagger UI, find the `/sentiment/analyze` endpoint under the "POST" section.

-   Click on it to expand the options.
-   Enter the text you want to analyze in the provided field (e.g., "testing API").
-   Click on `Execute` to send the request.

### Get All Sentiment Records:

-   Scroll to the /sentiment/all endpoint under the "GET" section.
-   Click on "Execute" to retrieve all sentiment records stored in the database.

## Running Unit Tests

o run the unit tests in the `tests/` directory, you can use `pytest` with the `PYTHONPATH` set to the current directory. This ensures that Python can locate the `app` module when running the tests.

### Set the `PYTHONPATH` and Run Tests

In the terminal, navigate to the root of your project (where `README.md` and `app/` are located), then run the following command:

```bash
PYTHONPATH=$(pwd) pytest tests/
```

### View the Test Results

After running the tests, you’ll see the output in the terminal. If all tests pass, you will see something like:

```bash
============================================================================ test session starts ============================================================================
platform darwin -- Python 3.12.4, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/leonjaggon/go/sentiment-api
plugins: anyio-4.8.0
collected 9 items

tests/test_endpoints.py .........                                                                                                                                     [100%]

============================================================================= 9 passed in 2.41s =============================================================================
```
