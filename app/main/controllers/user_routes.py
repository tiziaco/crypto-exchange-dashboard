from flask import request, jsonify
from flask import current_app as app

from ..services.user_service import save_new_user, get_all_users, get_a_user

@app.route('/add_user', methods=['POST'])
def add_user():
    """Creates a new User """
    user_data = request.json
    return save_new_user(data=user_data)

@app.route('/list_user', methods=['GET'])
def list_user():
    """List of registered user"""
    return get_all_users()