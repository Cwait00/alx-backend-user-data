#!/usr/bin/env python3
"""
SessionAuth module
"""

import uuid
from api.v1.auth.auth import Auth


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

    def current_user(self, request=None):
        """ Returns the current user by retrieving from session ID cookie """
        if request is None:
            return None
        session_cookie = request.cookies.get('_my_session_id')
        return self.user_id_by_session_cookie(session_cookie)

    def user_id_by_session_cookie(self, session_cookie_value):
        """
        Retrieve user ID based on session cookie value.

        Replace this mock implementation with actual logic to retrieve
        user ID from session data or database.
        """
        if session_cookie_value in self.user_id_by_session_id:
            return self.user_id_by_session_id[session_cookie_value]
        else:
            return None  # Invalid or expired session

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


if __name__ == "__main__":
    sa = SessionAuth()

    user_id_session_id_type = type(sa.user_id_by_session_id)
    print(f"{user_id_session_id_type}: {sa.user_id_by_session_id}")

    user_id = None
    session = sa.create_session(user_id)
    print(f"{user_id} => {session}: {sa.user_id_by_session_id}")

    user_id = 89
    session = sa.create_session(user_id)
    print(f"{user_id} => {session}: {sa.user_id_by_session_id}")

    user_id = "abcde"
    session = sa.create_session(user_id)
    print(f"{user_id} => {session}: {sa.user_id_by_session_id}")

    user_id = "fghij"
    session = sa.create_session(user_id)
    print(f"{user_id} => {session}: {sa.user_id_by_session_id}")

    user_id = "abcde"
    session = sa.create_session(user_id)
    print(f"{user_id} => {session}: {sa.user_id_by_session_id}")
