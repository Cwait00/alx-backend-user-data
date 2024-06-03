#!/usr/bin/env python3
"""
Auth module for handling authentication logic.

This module provides the Auth class, which serves as a template for managing
API authentication. It includes methods for handling authentication requirements,
authorization headers, and retrieving the current user.

Example usage:
    from api.v1.auth.auth import Auth

    a = Auth()

    # Check if authentication is required for a given path
    requires_auth = a.require_auth("/api/v1/status/", ["/api/v1/status/"])

    # Retrieve authorization header from Flask request
    auth_header = a.authorization_header()

    # Get current user object from Flask request
    current_user = a.current_user()
"""

from typing import List, TypeVar
from flask import request

class Auth:
    """
    Auth class for managing authentication in the API.

    Methods:
        require_auth(self, path: str, excluded_paths: List[str]) -> bool:
            Determines if authentication is required for a given path.

        authorization_header(self, request=None) -> str:
            Retrieves the authorization header from the Flask request.

        current_user(self, request=None) -> TypeVar('User'):
            Retrieves the current user object from the Flask request.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for a given path.

        Args:
            path (str): The path of the request.
            excluded_paths (List[str]): List of paths where authentication
            is not required.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            # Ensure paths are slash tolerant
            if path.endswith('/') and excluded_path == path:
                return False
            elif not path.endswith('/') and excluded_path == path + '/':
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the authorization header from the Flask request.

        Args:
            request (flask.Request, optional): The Flask request object.
            Defaults to None.

        Returns:
            str: The authorization header value.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user object from the Flask request.

        Args:
            request (flask.Request, optional): The Flask request object.
            Defaults to None.

        Returns:
            TypeVar('User'): The current user object.
        """
        return None
