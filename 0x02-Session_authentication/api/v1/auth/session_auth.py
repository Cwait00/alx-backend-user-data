#!/usr/bin/env python3
"""
SessionAuth module
"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    SessionAuth class that inherits from Auth
    """

    def authorization_header(self, request=None) -> str:
        """ Returns the value of the header request """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None):
        """ Returns the current user by retrieving from session ID cookie """
        if request is None:
            return None
        return self.user_id_by_session_cookie(request.cookies.get('_my_session_id'))

    def user_id_by_session_cookie(self, session_cookie_value):
        """
        Retrieve user ID based on session cookie value.

        Replace this mock implementation with actual logic to retrieve
        user ID from session data or database.
        """
        # Example mock implementation:
        if session_cookie_value == 'valid_session_id':
            return 'user123'  # Replace with actual user ID retrieval logic
        else:
            return None  # Invalid or expired session
