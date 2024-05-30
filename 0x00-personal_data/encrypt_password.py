#!/usr/bin/env python3
"""
Module for password encryption using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password string using bcrypt.

    Args:
        password: A string representing the password to be hashed.

    Returns:
        A salted, hashed password as a byte string.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against a hashed password using bcrypt.

    Args:
        hashed_password: A byte string representing the hashed password.
        password: A string representing the plain-text password to validate.

    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


if __name__ == "__main__":
    # Example usage
    password = "MyAmazingPassw0rd"
    hashed_password = hash_password(password)
    print(hashed_password.decode('utf-8'))
