from flask import jsonify
from app.main import db
from app.main.models.user import User
from app.main.models.portfolio import Portfolio, Transaction, Position
from app.main.services.user_service import get_user_id

def add_portfolio(user_public_id, portfolio_data):
    try:
        new_portfolio = Portfolio(
            name=portfolio_data.get('name'),
            exchange=portfolio_data.get('exchange'),
            user_id=get_user_id(user_public_id),
        )
        save_changes(new_portfolio)
        return {'status': 'success', 'message': 'Portfolio successfully added.'}, 200
    except Exception as e:
        db.session.rollback()
        return {'status': 'fail', 'message': str(e)}, 500

def remove_portfolio(user_public_id, portfolio_name):
    user_id=get_user_id(user_public_id)
    portfolio_to_delete = Portfolio.query.filter_by(user_id=user_id, 
                                                    name=portfolio_name).first()

    if portfolio_to_delete:
        db.session.delete(portfolio_to_delete)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'Portfolio "{portfolio_name}" deleted for user "{user_id}".'
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': f'Portfolio {portfolio_name} not found.',
        }
        return response_object, 404

def create_transaction(portfolio_id, transaction_data):
    portfolio = Portfolio.query.get(portfolio_id)
    transaction = Transaction(
            pair=transaction_data.get('pair'),
            side=transaction_data.get('side'),
            price=transaction_data.get('price'),
            quantity=transaction_data.get('quantity'),
            portfolio_id=portfolio.id
        )
    return transaction

def add_transaction_to_portfolio(portfolio_id, transaction_data):
    try:
        portfolio = Portfolio.query.get(portfolio_id)

        if not portfolio:
            return {'status': 'fail', 'message': 'Portfolio not found.'}, 404

        new_transaction = Transaction(
            pair=transaction_data.get('pair'),
            side=transaction_data.get('side'),
            price=transaction_data.get('price'),
            quantity=transaction_data.get('quantity'),
            portfolio_id=portfolio.id
        )
        save_changes(new_transaction)

        return {'status': 'success', 'message': 'Transaction successfully added.'}, 200
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return {'status': 'fail', 'message': str(e)}, 500

def remove_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)

        if not transaction:
            return {'status': 'fail', 'message': 'Transaction not found.'}, 404

        db.session.delete(transaction)
        db.session.commit()

        return {'status': 'success', 'message': f'Transaction ID {transaction.id} removed.'}, 200
    except Exception as e:
        db.session.rollback()
        return {'status': 'fail', 'message': str(e)}, 500

def get_portfolio_transactions(portfolio_id):
    try:
        transactions = Transaction.query.filter_by(portfolio_id=portfolio_id).all()

        # Optionally, serialize the transactions or return them as is
        serialized_transactions = [transaction.to_dict() for transaction in transactions]

        return jsonify(serialized_transactions), 200
    except Exception as e:
        return {'status': 'fail', 'message': str(e)}, 500

def get_portfolio_open_positions(portfolio_id):
    try:
        open_positions = Position.query.filter_by(portfolio_id=portfolio_id,
                                                is_open = True).all()
        # Optionally, serialize the transactions or return them as is
        serialized_positions = [position.to_dict() for position in open_positions]

        return jsonify(serialized_positions), 200
    except Exception as e:
        print(str(e))
        return {'status': 'fail', 'message': str(e)}, 500

def get_portfolio_closed_positions(portfolio_id):
    try:
        closed_positions = Position.query.filter_by(portfolio_id=portfolio_id,
                                                is_open = False).all()
        # Optionally, serialize the transactions or return them as is
        serialized_positions = [position.to_dict() for position in closed_positions]

        return jsonify(serialized_positions), 200
    except Exception as e:
        print(str(e))
        return {'status': 'fail', 'message': str(e)}, 500

def save_changes(data):
    db.session.add(data)
    db.session.commit()