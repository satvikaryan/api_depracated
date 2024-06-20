# Stock Price API

This application is a Flask-based web service that retrieves the current stock price for a given ticker symbol using the Alpha Vantage API. The application ensures secure access and proper request validation.

## Problem Statement

The goal of this application is to provide an easy and secure way to fetch real-time stock prices. Users can request the price of a specific stock by providing its ticker symbol. The application ensures the request is authenticated and handles errors gracefully, providing clear feedback on any issues encountered.

## API Endpoint

### `/api/stock`

**Method:** `POST`

**Description:** Retrieves the current stock price for a given ticker symbol.

**Request Headers:**
- `Authorization`: Bearer token required for authentication. The token value must be `mysecrettoken`.

**Request Body (JSON):**
- `ticker`: The ticker symbol of the stock (string).

**Responses:**

- `200 OK`: Returns the stock price.
  ```json
  {
      "AAPL": "150.00"
  }
  ```
- `400 Bad Request`: If the `ticker` is missing or not a string.
  ```json
  {
      "error": "Ticker symbol is required and must be a string"
  }
  ```
- `401 Unauthorized`: If the authorization header is missing or incorrect.
  ```json
  {
      "error": "Unauthorized"
  }
  ```
- `404 Not Found`: If the stock data or price is not found.
  ```json
  {
      "error": "Stock data not found"
  }
  ```
  ```json
  {
      "error": "Stock price not available"
  }
  ```
- `500 Internal Server Error`: If there is an issue fetching the stock price.
  ```json
  {
      "error": "Failed to fetch stock price"
  }
  ```

## Installation and Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/satvikaryan/api_endpoint
   cd api_endpoint
   ```

2. **Create a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Create a `config.py` file with your Alpha Vantage API key:**
   ```python
   # config.py
   API_KEY = 'your_alpha_vantage_api_key'
   ```

5. **Run the application:**
   ```sh
   flask run
   ```

## Usage Example

To fetch the stock price of a company with the ticker symbol "AAPL":

```sh
curl -X POST http://127.0.0.1:5000/api/stock \
-H "Content-Type: application/json" \
-H "Authorization: Bearer mysecrettoken" \
-d '{"ticker": "AAPL"}'
```

The response will be:

```json
{
    "AAPL": "150.00"
}
```

## Error Handling

The application includes robust error handling to ensure that users receive meaningful messages for various error conditions, such as missing authorization, incorrect request format, or issues with the external API.

## Conclusion

This application provides a secure and reliable way to fetch stock prices, making it a useful tool for anyone needing real-time stock data. The clear structure and comprehensive error handling make it user-friendly and robust.
