import unittest
from flask import json
from app.test.base import BaseTestCase
from app.main.models.user import User
from app.main.models.portfolio import Portfolio
from util import create_test_user, create_test_portfolio,\
    create_test_portfolio_with_transaction, create_test_portfolio_with_transactions

class PortfolioRoutesTest(BaseTestCase):

    def test_add_portfolio(self):
        # Create a user to associate the portfolio with
        user = create_test_user()

        # Make a request to add a portfolio
        response = self.client.post(
            f'/{user.public_id}/portfolio/add',
            data=json.dumps({
                'name': 'Test Portfolio',
                'exchange': 'Binance Test'
            }),
            content_type='application/json'
        )
        self.assert200(response)
        self.assertIn('Portfolio successfully added.', response.json['message'])

        # Verify that the portfolio is in the database
        user_portfolios = User.query.get(user.id).portfolios
        self.assertEqual(len(user_portfolios), 1)
        self.assertEqual(user_portfolios[0].name, 'Test Portfolio')
    
    def test_delete_portfolio(self):
        # Create a test user and portfolio
        user = create_test_user()
        portfolio = create_test_portfolio(user.id)

        # Make a request to delete the portfolio
        response = self.client.delete(f'/{user.public_id}/portfolio/delete/{portfolio.name}')
        self.assert200(response)
        self.assertIn(f'Portfolio "{portfolio.name}" deleted for user "{user.id}".', response.json['message'])

        # Verify that the portfolio is no longer in the database
        deleted_portfolio = Portfolio.query.filter_by(id=portfolio.id).first()
        self.assertIsNone(deleted_portfolio)
    
    def test_add_transaction(self):
        # Create a portfolio to associate the transaction with
        user = create_test_user()
        portfolio = create_test_portfolio(user.id)

        # Make a request to add a transaction
        response = self.client.post(
            f'/add_transaction/{portfolio.id}',
            data=json.dumps({
                'date': '2023-01-01T12:00:00Z',
                'pair': 'BTC/USD',
                'side': 'buy',
                'price': 50000,
                'quantity': 1,
                'amount': 50000
            }),
            content_type='application/json'
        )
        self.assert200(response)
        self.assertIn('Transaction successfully added.', response.json['message'])
    
    def test_remove_transaction(self):
        # Create a portfolio and a transaction for testing removal
        portfolio, transaction = create_test_portfolio_with_transaction()

        # Test removing a transaction
        response = self.client.delete(f'/delete_transaction/{portfolio.id}/{transaction.id}')
        self.assert200(response)
        self.assertIn(f'Transaction ID {transaction.id} removed.', response.json['message'])
    
    def test_get_transactions(self):
        # Create a portfolio and transactions for testing retrieval
        portfolio, transactions = create_test_portfolio_with_transactions()

        # Test getting portfolio transactions
        response = self.client.get(f'/get_transactions/{portfolio.id}')
        self.assert200(response)
        self.assertEqual(len(response.json), len(transactions))

if __name__ == '__main__':
    unittest.main()
