from flask import request, Blueprint

from ..services.user_service import save_new_user, get_all_users, remove_user, \
get_user_portfolios

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/add_user', methods=['POST'])
def add_user():
    """Creates a new User """
    user_data = request.json
    return save_new_user(data=user_data)

@user_blueprint.route('/list_user', methods=['GET'])
def list_user():
    """List of registered user"""
    return get_all_users()

@user_blueprint.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """List of registered user"""
    return remove_user(user_id)

@user_blueprint.route('/<string:user_public_id>/get_portfolios', methods=['GET'])
def get_portfolios(user_public_id):
    """List of registered user"""
    return get_user_portfolios(user_public_id)