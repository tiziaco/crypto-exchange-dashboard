import uuid
import datetime

from app.main import db
from app.main.models.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'User successfully registered.'
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

def get_all_users():
    return User.query.all()

def get_a_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if user:
        return user
    else:
        response_object = {
            'status': 'fail',
            'message': 'User not found',
        }
        return response_object, 409

def remove_user(user_id):
    user_to_delete = User.query.get(user_id)

    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'User ID {user_id} deleted.'
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': f'User ID {user_id} not found.',
        }
        return response_object, 404

def save_changes(data):
    db.session.add(data)
    db.session.commit()