#!/usr/bin/env python3
""" Auth class for API authentication """
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth class template """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method for authentication requirement """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
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
