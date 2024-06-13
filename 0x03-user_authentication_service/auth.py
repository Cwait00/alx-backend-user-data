#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    Hash a password with bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def _generate_uuid() -> str:
    """
    Generate a new UUID.

    Returns:
        str: The string representation of the generated UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The newly created user.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login credentials.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            bool: True if login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if (user and bcrypt.checkpw(password.encode(),
                                        user.hashed_password)):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """
        Create a session for the user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID, or None if user not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Get a user by session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            Optional[User]: The user if found, None otherwise.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session.

        Args:
            user_id (int): The ID of the user.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If no user found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"No user found with email {email}")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_pwd,
                reset_token=None
            )
        except NoResultFound:
            raise ValueError("Invalid reset token")
