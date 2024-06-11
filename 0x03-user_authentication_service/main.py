#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User
from auth import Auth, _hash_password
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def print_user_table_info():
    """Print the table name and columns for the User model."""
    print(User.__tablename__)
    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))


def test_add_user():
    """Test adding users to the database and print their IDs."""
    my_db = DB()
    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(user_1.id)
    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(user_2.id)


def test_find_user_by():
    """Test finding users by email and handle exceptions."""
    my_db = DB()
    user = my_db.add_user("test@test.com", "PwdHashed")
    print(user.id)
    try:
        find_user = my_db.find_user_by(email="test@test.com")
        print(find_user.id)
    except NoResultFound:
        print("Not found")
    try:
        find_user = my_db.find_user_by(email="test2@test.com")
        print(find_user.id)
    except NoResultFound:
        print("Not found")
    try:
        find_user = my_db.find_user_by(no_email="test@test.com")
        print(find_user.id)
    except InvalidRequestError:
        print("Invalid")


def test_update_user():
    """Test updating a user's password."""
    my_db = DB()
    email = 'test@test.com'
    hashed_password = "hashedPwd"
    user = my_db.add_user(email, hashed_password)
    print(user.id)
    try:
        my_db.update_user(user.id, hashed_password='NewPwd')
        print("Password updated")
    except ValueError:
        print("Error")


def test_hash_password():
    """Test hashing a password."""
    print(_hash_password("Hello Holberton"))


def test_register_user():
    """Test registering a user and handle potential errors."""
    email = 'me@me.com'
    password = 'mySecuredPwd'
    auth = Auth()
    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print("could not create a new user: {}".format(err))
    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print("could not create a new user: {}".format(err))


def test_valid_login():
    """Test validating login credentials."""
    email = 'bob@bob.com'
    password = 'MyPwdOfBob'
    auth = Auth()
    auth.register_user(email, password)
    print(auth.valid_login(email, password))
    print(auth.valid_login(email, "WrongPwd"))
    print(auth.valid_login("unknown@email", password))


def test_create_session():
    """Test creating a session and handling non-existing user."""
    auth = Auth()
    email = 'bob@bob.com'
    auth.register_user(email, 'MyPwdOfBob')
    print(auth.create_session(email))
    print(auth.create_session("unknown@email.com"))


if __name__ == "__main__":
    print_user_table_info()
    test_add_user()
    test_find_user_by()
    test_update_user()
    test_hash_password()
    test_register_user()
    test_valid_login()
    test_create_session()
