#!/usr/bin/env python3
"""
SessionAuth views
"""

import os
from flask import request, jsonify, abort
from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuth
from models.user import User
import logging

auth = SessionAuth()

logging.basicConfig(level=logging.DEBUG)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles the login for Session Authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    logging.debug(f'Login attempt with email: {email}')

    user = User.search({"email": email})
    logging.debug(f'User search result: {user}')

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    logging.debug(f'Session ID created: {session_id}')

    response = jsonify(user.to_json())
    session_name = os.getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)
    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def logout():
    """
    Handles the logout for Session Authentication
    """
    logging.debug('Logout attempt')

    if not auth.destroy_session(request):
        abort(404)

    logging.debug('Logout successful')
    return jsonify({}), 200
