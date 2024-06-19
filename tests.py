# tests.py

import unittest
import json
from unittest.mock import patch, MagicMock
from app import app
import requests
class TestStockAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_unauthorized_access(self):
        # Test unauthorized access without Authorization header
        response = self.app.post('/api/stock')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'Unauthorized')

        # Test unauthorized access with incorrect Authorization header
        response = self.app.post('/api/stock', headers={'Authorization': 'Bearer wrongtoken'})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'Unauthorized')

    def test_missing_ticker_symbol(self):
        # Test when ticker symbol is not provided
        response = self.app.post('/api/stock', headers={'Authorization': 'Bearer mysecrettoken'}, json={})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Ticker symbol is required and must be a string')

    def test_ticker_symbol_not_string(self):
        # Test when ticker symbol is not a string
        response = self.app.post('/api/stock', headers={'Authorization': 'Bearer mysecrettoken'}, json={'ticker': 123})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Ticker symbol is required and must be a string')

    @patch('requests.get')
    def test_get_stock_price(self, mock_get):
        # Mocking the response from Alpha Vantage API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Global Quote": {
                "05. price": "189.05"
            }
        }
        mock_get.return_value = mock_response

        # Test successful retrieval of stock price
        response = self.app.post('/api/stock', headers={'Authorization': 'Bearer mysecrettoken'}, json={'ticker': 'AAPL'})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('AAPL', data)
        self.assertEqual(data['AAPL'], '189.05')

    @patch('requests.get')
    def test_failed_stock_price_fetch(self, mock_get):
        # Mocking the response for failed fetch from Alpha Vantage API
        mock_get.side_effect = requests.exceptions.RequestException

        # Test when fetching stock price fails
        response = self.app.post('/api/stock', headers={'Authorization': 'Bearer mysecrettoken'}, json={'ticker': 'AAPL'})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['error'], 'Failed to fetch stock price')

    @patch('requests.get')
    def test_stock_data_not_found(self, mock_get):
        # Mocking the response for stock data not found
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        # Test when stock data is not found
        response = self.app.post('/api/stock', headers={'Authorization': 'Bearer mysecrettoken'}, json={'ticker': 'AAPL'})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Stock data not found')

    @patch('requests.get')
    def test_stock_price_not_available(self, mock_get):
        # Mocking the response where stock price is not available
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Global Quote": {}
        }
        mock_get.return_value = mock_response

        # Test when stock price is not available
        response = self.app.post('/api/stock', headers={'Authorization': 'Bearer mysecrettoken'}, json={'ticker': 'AAPL'})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Stock price not available')

if __name__ == '__main__':
    unittest.main()