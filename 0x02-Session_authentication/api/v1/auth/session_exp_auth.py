#!/usr/bin/env python3
"""
SessionExpAuth module

This module defines the SessionExpAuth class, which extends SessionAuth
to include session expiration functionality based on a configurable duration.
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that adds expiration to sessions.

    Inherits from SessionAuth and extends it by adding session expiration
    based on a configured session duration.
    """

    def __init__(self):
        """
        Initialize the SessionExpAuth class.

        Sets up the session duration based on the SESSION_DURATION environment
        variable. If SESSION_DURATION is not set or cannot be parsed as an
        integer, session duration is set to 0 (no expiration).
        """
        super().__init__()
        session_duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session ID with an expiration.

        Overrides the create_session method from SessionAuth to include
        storing session creation time for later expiration checking.

        Args:
            user_id (str): The user ID associated with the session.

        Returns:
            str: The generated session ID.
            None: If session creation fails.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return user ID if session is not expired.

        Checks if the session identified by session_id exists and is not
        expired based on the session creation time and configured
        session_duration.

        Args:
            session_id (str): The session ID to lookup.

        Returns:
            str: The user ID associated with the session if valid
            and not expired.
            None: If session is expired or does not exist.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session_dict.get("user_id")
