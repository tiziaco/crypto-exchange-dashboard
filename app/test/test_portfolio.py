import unittest
from flask import json
from datetime import datetime
from app.test.base import BaseTestCase
from app.main.models.user import User
from app.main import db

class PortfolioRoutesTest(BaseTestCase):

    def test_add_portfolio(self):
        # Create a user to associate the portfolio with
        user = User(username='test_user', 
                    email='test@example.com', 
                    password='12345',
                    registered_on=datetime.utcnow()
                    )
        db.session.add(user)
        db.session.commit()

        user_id = user.id

        # Test adding a portfolio
        response = self.client.post(
            f'/add_portfolio/{user_id}',
            data=json.dumps({
                'name': 'Test Portfolio',
                'exchange' : 'Binance'
            }),
            content_type='application/json'
        )

        self.assert200(response)  # Expecting a successful response
        self.assertIn('Portfolio successfully added.', response.json['message'])

        # Verify that the portfolio is in the database
        user_portfolios = User.query.get(user_id).portfolios
        self.assertEqual(len(user_portfolios), 1)
        self.assertEqual(user_portfolios[0].name, 'Test Portfolio')

if __name__ == '__main__':
    unittest.main()
