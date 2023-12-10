import uuid
import datetime

from app.main import db
from app.main.models.user import User
from app.main.models.portfolio import Portfolio

def add_portfolio(user_id, portfolio_data):
    try:
        new_portfolio = Portfolio(
            name=portfolio_data.get('name'),
            exchange=portfolio_data.get('exchange'),
            user_id=user_id,
        )
        save_changes(new_portfolio)
        return {'status': 'success', 'message': 'Portfolio successfully added.'}, 200
    except Exception as e:
        db.session.rollback()
        return {'status': 'fail', 'message': str(e)}, 500

def remove_portfolio(user_id, portfolio_name):
    portfolio_to_delete = Portfolio.query.filter_by(user_id=user_id, 
                                                    name=portfolio_name).first()

    if portfolio_to_delete:
        db.session.delete(portfolio_to_delete)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'Portfolio {portfolio_name} deleted.'
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': f'Portfolio {portfolio_name} not found.',
        }
        return response_object, 404

def save_changes(data):
    db.session.add(data)
    db.session.commit()