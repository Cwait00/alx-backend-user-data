#!/usr/bin/env python3
""" Auth class for API authentication """
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """ Auth class template """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method for authentication requirement """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                base_path = excluded_path.rstrip('*')
                if path.startswith(base_path):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method for authorization header """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method for current user """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
