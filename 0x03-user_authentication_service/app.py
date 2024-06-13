#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=["GET"])
def welcome():
    """GET / route
    Return:
      - JSON payload {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """POST /users route
    Register a user.
    Return:
      - JSON payload {"email": "<registered email>", "message": "user created"}
      - JSON payload {"message": "email already registered"} with a 400
      status code if the email is already registered
    """
    email = request.form.get("email")
    password = request.form.get("password")
    
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """POST /sessions route
    Log in a user.
    Return:
      - JSON payload {"email": "<user email>", "message": "logged in"}
      - 401 HTTP status if login information is incorrect
    """
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not AUTH.valid_login(email, password):
        abort(401)
    
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """DELETE /sessions route
    Log out a user.
    Return:
      - Redirect to GET /
      - 403 HTTP status if the session ID is invalid
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id or not AUTH.get_user_from_session_id(session_id):
        abort(403)
    
    AUTH.destroy_session(session_id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """GET /profile route
    Get the profile of a user.
    Return:
      - JSON payload {"email": "<user email>"}
      - 403 HTTP status if the session ID is invalid
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    
    if not user:
        abort(403)
    
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """POST /reset_password route
    Get a reset password token.
    Return:
      - JSON payload {"email": "<user email>", "reset_token": "<reset token>"}
      - 403 HTTP status if the email is not registered
    """
    email = request.form.get("email")
    
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """PUT /reset_password route
    Update the password of a user.
    Return:
      - JSON payload {"email": "<user email>", "message": "Password updated"}
      - 403 HTTP status if the token is invalid
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
