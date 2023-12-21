import unittest
from flask import json
from app.test.base import BaseTestCase
from app.main.models.portfolio import Portfolio
from util import create_empty_portfolio

class PositionsRoutesTest(BaseTestCase):

    def transact_buy(self, price, quantity, portfolio):
        self.client.post(
            f'/add_transaction/{portfolio.id}',
            data=json.dumps({
                'date': '2023-01-01T12:00:00Z',
                'pair': 'BTC/USD',
                'side': 'buy',
                'price': price,
                'quantity': quantity,
            }),
            content_type='application/json')
    
    def transact_sell(self, price, quantity, portfolio):
        self.client.post(
            f'/add_transaction/{portfolio.id}',
            data=json.dumps({
                'date': '2023-01-02T12:00:00Z',
                'pair': 'BTC/USD',
                'side': 'sell',
                'price': price,
                'quantity': quantity,
            }),
            content_type='application/json')
    
    def test_long_position(self):
        # Create a portfolio for testing retrieval
        portfolio = create_empty_portfolio()

        # Transact buy
        self.transact_buy(50000,1,portfolio)
        # Transact sell
        self.transact_sell(60000,1,portfolio)

        # Test getting portfolio open positions
        response = self.client.get(f'/get_closed_positions/{portfolio.id}')
        self.assert200(response)
        positions = response.json
        position = positions[0]

        self.assertIsInstance(positions, list)
        self.assertEqual(len(positions), 1)
        self.assertEqual(position["is_open"], False)
        self.assertEqual(position["side"], "long")
        self.assertEqual(position["buy_quantity"], 1)
        self.assertEqual(position["sell_quantity"], 1)
        self.assertEqual(position["avg_bought"], 50000)
        self.assertEqual(position["avg_sold"], 60000)
        self.assertEqual(position["avg_price"], 0)
        self.assertEqual(position["total_bought"], 50000)
        self.assertEqual(position["total_sold"], 60000)
        self.assertEqual(position["net_total"], 10000)
        self.assertEqual(position["realised_pnl"], 10000)
        self.assertEqual(position["unrealised_pnl"], 0)
    
    def test_short_position(self):
        # Create a portfolio for testing retrieval
        portfolio = create_empty_portfolio()

        # Transact sell
        self.transact_sell(60000,1,portfolio)
        # Transact buy
        self.transact_buy(50000,1,portfolio)
        
        # Test getting portfolio open positions
        response = self.client.get(f'/get_closed_positions/{portfolio.id}')
        self.assert200(response)
        ## TEST
        response_data = response.get_json()
        if response_data and 'message' in response_data:
            print(response_data['message'])

        positions = response.json
        position = positions[0]

        self.assertIsInstance(positions, list)
        self.assertEqual(len(positions), 1)
        self.assertEqual(position["is_open"], False)
        self.assertEqual(position["side"], "short")
        self.assertEqual(position["buy_quantity"], 1)
        self.assertEqual(position["sell_quantity"], 1)
        self.assertEqual(position["net_quantity"], 0)
        self.assertEqual(position["avg_bought"], 50000)
        self.assertEqual(position["avg_sold"], 60000)
        self.assertEqual(position["avg_price"], 0)
        self.assertEqual(position["total_bought"], 50000)
        self.assertEqual(position["total_sold"], 60000)
        self.assertEqual(position["net_total"], 10000)
        self.assertEqual(position["realised_pnl"], 10000)
        self.assertEqual(position["unrealised_pnl"], 0)

# Test with multiple buy or sell
    def test_long_position_multiple_buy(self):
        # Create a portfolio for testing retrieval
        portfolio = create_empty_portfolio()

        # Transact buy
        self.transact_buy(50000,1,portfolio)
        self.transact_buy(40000,2,portfolio)
        # Transact sell
        #self.transact_sell(60000,1,portfolio)

        # Test getting portfolio open positions
        response = self.client.get(f'/get_open_positions/{portfolio.id}')
        self.assert200(response)
        positions = response.json
        position = positions[0]

        self.assertIsInstance(positions, list)
        self.assertEqual(len(positions), 1)
        self.assertEqual(position["is_open"], True)
        self.assertEqual(position["side"], "long")
        self.assertEqual(position["current_price"], 40000)
        self.assertEqual(position["buy_quantity"], 3)
        self.assertEqual(position["sell_quantity"], 0)
        self.assertAlmostEqual(position["avg_bought"], 43333.3333, delta=0.0001)
        self.assertEqual(position["avg_sold"], 0)
        self.assertAlmostEqual(position["avg_price"], 43333.3333, delta=0.0001)
        self.assertEqual(position["total_bought"], 130000)
        self.assertEqual(position["total_sold"], 0)
        self.assertEqual(position["net_total"], -10000)
        self.assertEqual(position["realised_pnl"], 0)
        self.assertAlmostEqual(position["unrealised_pnl"], -10000, delta=0.0001)

    def test_short_position_multiple_sell(self):
        # Create a portfolio for testing retrieval
        portfolio = create_empty_portfolio()

        # Transact buy
        self.transact_sell(50000,1,portfolio)
        self.transact_sell(40000,2,portfolio)
        # Transact sell
        #self.transact_sell(60000,1,portfolio)

        # Test getting portfolio open positions
        response = self.client.get(f'/get_open_positions/{portfolio.id}')
        self.assert200(response)
        positions = response.json
        position = positions[0]

        self.assertIsInstance(positions, list)
        self.assertEqual(len(positions), 1)
        self.assertEqual(position["is_open"], True)
        self.assertEqual(position["side"], "short")
        self.assertEqual(position["current_price"], 40000)
        self.assertEqual(position["buy_quantity"], 0)
        self.assertEqual(position["sell_quantity"], 3)
        self.assertAlmostEqual(position["avg_bought"], 0, delta=0.0001)
        self.assertAlmostEqual(position["avg_sold"], 43333.3333, delta=0.0001)
        self.assertAlmostEqual(position["avg_price"], 43333.3333, delta=0.0001)
        self.assertEqual(position["total_bought"], 0)
        self.assertEqual(position["total_sold"], 130000)
        self.assertEqual(position["net_total"], 10000)
        self.assertEqual(position["realised_pnl"], 0)
        self.assertAlmostEqual(position["unrealised_pnl"], 10000, delta=0.0001)


if __name__ == '__main__':
    unittest.main()
