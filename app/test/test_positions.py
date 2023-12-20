import unittest
from flask import json
from app.test.base import BaseTestCase
from app.main.models.user import User
from app.main.models.portfolio import Portfolio
from util import create_test_user, create_test_portfolio,\
    create_test_portfolio_with_transaction, create_test_portfolio_with_transactions

class PositionsRoutesTest(BaseTestCase):
    
    def test_long_position(self):
        # Create a portfolio and transactions for testing retrieval
        portfolio, transactions = create_test_portfolio_with_transactions()

        # Test getting portfolio open positions
        response = self.client.get(f'/get_open_positions/{portfolio.id}')
        self.assert200(response)
        positions = response.json
        position = positions[0]

        self.assertIsInstance(positions, list)
        self.assertEqual(len(positions), 1)
        #self.assertEqual(position["is_open"], False)
        self.assertEqual(position["side"], "long")
        self.assertEqual(position["avg_price"], 50000)
        self.assertEqual(position["net_quantity"], 0)
        self.assertEqual(position["net_total"], -50000)
        self.assertEqual(position["realised_pnl"], 10000)
        self.assertEqual(position["unrealised_pnl"], 0)

if __name__ == '__main__':
    unittest.main()
