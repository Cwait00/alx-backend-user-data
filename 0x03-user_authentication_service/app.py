#!/usr/bin/env python3
"""
Flask application module
"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/')
def welcome():
    """Welcome route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/register', methods=['POST'])
def register_user():
    """Registers a new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    try:
        user = auth.register_user(email, password)
        return jsonify({"email": user.email}), 201
    except Exception:
        return jsonify({"error": "User already exists"}), 400


@app.route('/login', methods=['POST'])
def login():
    """Logs in a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    response = jsonify({"message": "Login successful"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/logout', methods=['DELETE'])
def logout():
    """Logs out a user"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    auth.destroy_session(user.id)
    return redirect(url_for('welcome'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
