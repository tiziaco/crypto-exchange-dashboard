from flask import Blueprint, request
from app.main.services.portfolio_service import add_portfolio, remove_portfolio,\
add_transaction_to_portfolio, remove_transaction, get_portfolio_transactions
#from flask import current_app as app

portfolio_blueprint = Blueprint('portfolio', __name__)

@portfolio_blueprint.route('/<string:user_public_id>/portfolio/add', methods=['POST'])
def create_portfolio(user_public_id):
	portfolio_data = request.json
	return add_portfolio(user_public_id, portfolio_data)

@portfolio_blueprint.route('/<string:user_public_id>/portfolio/delete/<string:portfolio_name>', methods=['DELETE'])
def delete_portfolio(user_public_id, portfolio_name):
    """List of registered user"""
    return remove_portfolio(user_public_id, portfolio_name)

@portfolio_blueprint.route('/add_transaction/<int:portfolio_id>', methods=['POST'])
def add_transaction(portfolio_id):
    transaction_data = request.json
    return add_transaction_to_portfolio(portfolio_id, transaction_data)

@portfolio_blueprint.route('/delete_transaction/<int:portfolio_id>/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(portfolio_id, transaction_id):
    return remove_transaction(transaction_id)

@portfolio_blueprint.route('/get_transactions/<int:portfolio_id>', methods=['GET'])
def get_transactions(portfolio_id):
    return get_portfolio_transactions(portfolio_id)