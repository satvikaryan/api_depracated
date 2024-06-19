from flask import Flask, request, jsonify
import requests
import os
from config import API_KEY

app = Flask(__name__)

@app.route('/api/stock', methods=['POST'])
def get_stock_price():
    # Check for authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer mysecrettoken':
        return jsonify({'error': 'Unauthorized'}), 401

    # Parse JSON request body
    data = request.get_json()
    if not data or 'ticker' not in data or not isinstance(data['ticker'], str):
        return jsonify({'error': 'Ticker symbol is required and must be a string'}), 400

    ticker = data['ticker']
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"

    # Make the request to the external API
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Failed to fetch stock price'}), 500

    stock_data = response.json()
    if 'Global Quote' not in stock_data:
        return jsonify({'error': 'Stock data not found'}), 404

    stock_price = stock_data['Global Quote'].get('05. price')
    if not stock_price:
        return jsonify({'error': 'Stock price not available'}), 404

    return jsonify({ticker: stock_price})

if __name__ == '__main__':
    app.run(debug=True)
