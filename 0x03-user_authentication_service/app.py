#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth
import logging

app = Flask(__name__)

# Instantiate the Auth object
AUTH = Auth()

# Suppress SQLAlchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


@app.route("/", methods=["GET"])
def index():
    """Return a JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Register a new user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
