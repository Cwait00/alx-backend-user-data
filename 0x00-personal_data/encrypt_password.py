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

if __name__ == "__main__":
    # Example usage
    password = "MyAmazingPassw0rd"
    hashed_password = hash_password(password)
    print(hashed_password.decode('utf-8'))
