#!/usr/bin/env python3
"""
Auth module for the API
"""
from typing import List, TypeVar
from flask import request

class Auth:
    """Auth class for handling authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if the path requires authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path[-1] != '/':
                excluded_path += '/'
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieve the authorization header from the request"""
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the current user"""
        return None
