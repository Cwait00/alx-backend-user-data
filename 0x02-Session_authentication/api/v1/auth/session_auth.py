#!/usr/bin/env python3
"""
SessionAuth module
"""

import uuid
import os  # Importing os module to use os.getenv
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class that inherits from Auth
    """

    user_id_by_session_id = {}  # Class attribute to store session ID mappings

    def authorization_header(self, request=None) -> str:
        """ Returns the value of the header request """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        if session_name is None:
            return None
        return request.cookies.get(session_name)

    def current_user(self, request=None):
        """ Returns the current user by retrieving from session ID cookie """
        if request is None:
            return None
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None
        return User.get(user_id)

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): The user ID to associate with the Session ID.

        Returns:
            str: The generated Session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.

        Args:
            session_id (str): The Session ID to look up.

        Returns:
            str: The User ID associated with the Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session / logout.

        Args:
            request (flask.Request): The request object containing the
            session ID cookie.

        Returns:
            bool: True if the session was successfully destroyed,
            False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
