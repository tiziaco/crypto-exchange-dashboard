import unittest
from flask import json
from app.test.base import BaseTestCase
from app.main.models.user import User
from app.main import db
from util import create_test_user, create_test_portfolio

class UserRoutesTest(BaseTestCase):

    def test_app_is_running(self):
        # Test if the app is running by sending a GET request to a known route
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        # Test adding a user
        response = self.client.post(
            '/add_user',
            data=json.dumps({
                'username': 'test_user',
                'email': 'test@example.com',
                'password': '12345'
            }),
            content_type='application/json'
        )
        self.assert200(response)
        self.assertIn('User successfully registered.', response.json['message'])

        # Verify that the user is in the database
        user = User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

    def test_delete_user(self):
        # Create a user for testing deletion
        new_user = create_test_user()

        # Test deleting a user
        user_id = new_user.id
        response = self.client.delete(f'/delete_user/{user_id}')
        self.assert200(response)
        self.assertIn(f'User ID {user_id} deleted.', response.json['message'])

        # Verify that the user is no longer in the database
        user = User.query.get(user_id)
        self.assertIsNone(user)

    def test_delete_nonexistent_user(self):
        # Test deleting a user that does not exist
        response = self.client.delete('/delete_user/999')
        print(response)
        self.assert404(response)
        self.assertIn('User ID 999 not found.', response.json['message'])

    def test_get_user_portfolios(self):
        user = create_test_user()
        portfolio = create_test_portfolio(user.id)

        response = self.client.get(f'/{user.public_id}/get_portfolios')
        self.assert200(response)

if __name__ == '__main__':
    unittest.main()
