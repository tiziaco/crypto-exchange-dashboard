import uuid
import datetime

from server.main import db
from server.main.models.user import User


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
            'message': 'Successfully registered.'
        }
        return response_object, 201
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

def delete_user(public_id):
    user_to_delete = User.query.get(public_id)

    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'User deleted.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User not found.',
        }
        return response_object, 409

def save_changes(data):
    db.session.add(data)
    db.session.commit()