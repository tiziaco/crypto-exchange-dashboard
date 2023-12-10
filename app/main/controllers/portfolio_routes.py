from flask import Blueprint, request
from app.main.services.portfolio_service import add_portfolio, remove_portfolio
from flask import current_app as app

portfolio_blueprint = Blueprint('portfolio', __name__)

@portfolio_blueprint.route('/add_portfolio/<int:user_id>', methods=['POST'])
def create_portfolio(user_id):
	portfolio_data = request.json
	return add_portfolio(user_id, portfolio_data)

@portfolio_blueprint.route('/delete_portfolio/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """List of registered user"""
    return remove_portfolio(user_id)