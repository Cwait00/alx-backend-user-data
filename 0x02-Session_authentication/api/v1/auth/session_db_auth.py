#!/usr/bin/env python3
"""
SessionDBAuth module: defines SessionDBAuth class that handles session
authentication with database storage.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from flask import request
import uuid


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class handles session authentication with database storage.

    Inherits from SessionExpAuth for session expiration functionality.
    """

    def __init__(self):
        """
        Initializes a new instance of SessionDBAuth with an empty session
        database.
        """
        self._db = {}

    def create_session(self, user_id=None):
        """
        Create a session ID and store it in the database.

        Args:
            user_id (str): The ID of the user for whom the session is created.

        Returns:
            str: The session ID created.

        Notes:
            If user_id is None, returns None.
        """
        if user_id is None:
            return None

        session_id = str(uuid.uuid4())
        new_session = UserSession(user_id=user_id, session_id=session_id)
        self._db[session_id] = new_session
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve user ID associated with a session ID from the database.

        Args:
            session_id (str): The session ID to look up in the database.

        Returns:
            str: The user ID associated with the session ID if found,
            otherwise None.

        Notes:
            If session_id is None or not found in the database, returns None.
        """
        if session_id is None:
            return None

        session_dict = self._db.get(session_id)
        if session_dict is None:
            return None

        return session_dict.user_id

    def destroy_session(self, request=None):
        """
        Destroy a session based on the Session ID from the request cookie.

        Args:
            request (Request): The Flask request object containing session
            ID in cookie.

        Returns:
            bool: True if session was successfully destroyed, False otherwise.

        Notes:
            If request is None or session ID is not found in the database,
            returns False.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        session_dict = self._db.get(session_id)
        if not session_dict:
            return False

        del self._db[session_id]
        return True
