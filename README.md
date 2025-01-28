# Sentiment Analysis API

A Dockerized FastAPI application for analyzing text sentiment and retrieving recent analyses.

## Features

- **POST /analyze**: Analyze the sentiment of a text input.
- **GET /recent**: Retrieve the 5 most recent sentiment analyses.
- Docker support for easy deployment and scalability.

## Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LeonJaggons/sentiment-api.git
   cd sentiment-api
   ```

2. Build the Docker image with:

   ```bash
   make build
   ```

### Running the API

1. Start the API service with:

   ```bash
   make start
   ```

The API will be available at `http://localhost:80` by default.

### Access the API Documentation

Navigate to `http://localhost:80/docs` to interact with the API endpoints via Swagger UI.

## API Endpoints

### 1. Analyze text sentiment

- **Endpoint**: `POST /analyze`

- **Description**: Analyze the sentiment of a text string

- **Request Body**:

  ```json
  {
    "text": "i've created the best sentiment-api every made!"
  }
  ```

- **Response**:

  ```json
  {
    "text": "i've created the best sentiment-api every made!",
    "sentiment": "POSITIVE",
    "confidence_score": 0.997597873210907,
    "created_at": "2025-01-28T11:16:13.416354"
  }
  ```

### 2. Get recent text sentiment analyses

- **Endpoint**: `GET /recent`

- **Description**: Get the 5 most recent sentiment analyses performed by the API

- **Response**:

  ```json
  [
    {
      "text": "i've created the most alright sentiment-api ever made... i guess ",
      "sentiment": "POSITIVE",
      "confidence_score": 0.9548478126525879,
      "created_at": "2025-01-28T11:18:52.753227"
    },
    {
      "text": "i've created the worst sentiment-api ever made.... ",
      "sentiment": "NEGATIVE",
      "confidence_score": 0.999815046787262,
      "created_at": "2025-01-28T11:18:32.479823"
    },
    {
      "text": "i've created the best sentiment-api every made!",
      "sentiment": "POSITIVE",
      "confidence_score": 0.997597873210907,
      "created_at": "2025-01-28T11:16:13.416354"
    }
  ]
  ```

### 3. Clear text sentiment analyses

- **Endpoint**: `POST /recent/clear`

- **Description**: Clear all recent text sentiments analyzed and stored by the API

- **Response**:

  ```json
  {
    "message": "Recent sentiments cleared"
  }
  ```

  ```json
  # `GET /recent`
  []
  ```

## Example Usage

While the API can be used directly from the Swagger UI available at `http://localhost/docs`, here are some examples using cURL

### 1. Analyze text sentiment

```bash
curl -X 'POST' \
  'http://localhost/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "this cURL command will access the most alright sentiment-api ever made... i guess.. hopefully "
}'
```

### 2. Get recent text sentiment analyses

```bash
curl -X 'GET' \
  'http://localhost/recent' \
  -H 'accept: application/json'
```

### 3. Clear text sentiment analyses

```bash
curl -X 'POST' \
  'http://localhost/recent/clear' \
  -H 'accept: application/json' \
  -d ''
```

## Testing

To test with pytest, we have to ensure the container is running and proceed to exec into it using the commands available in the Makefile. After this, we are able to run the `pytest` command as normal.

1. Start the API service using:

   ```bash
   make start
   ```

2. Execute into the API service's running container with:

   ```bash
   make bash
   ```

3. Run `pytest` inside the container with:

   ```bash
   pytest -v
   ```