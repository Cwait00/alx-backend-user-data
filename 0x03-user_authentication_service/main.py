#!/usr/bin/env python3
"""
Main file for testing DB module functionalities and password hashing
"""
from user import User
from db import DB
from auth import Auth, _hash_password
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def print_user_table_info() -> None:
    """Print information about the User table"""
    print(User.__tablename__)
    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))


def test_add_user() -> None:
    """Test the add_user method of DB class"""
    my_db = DB()
    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(user_1.id)

    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(user_2.id)


def test_find_user_by() -> None:
    """Test the find_user_by method of DB class"""
    my_db = DB()
    user = my_db.add_user("test@test.com", "PwdHashed")
    print(user.id)

    find_user = my_db.find_user_by(email="test@test.com")
    print(find_user.id)

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


def test_update_user() -> None:
    """Test the update_user method of DB class"""
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


def test_hash_password() -> None:
    """Test the _hash_password method"""
    print(_hash_password("Hello Holberton"))


def test_register_user() -> None:
    """Test the register_user method of Auth class"""
    email = 'me@me.com'
    password = 'mySecuredPwd'
    auth = Auth()

    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print(f"could not create a new user: {err}")

    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print(f"could not create a new user: {err}")


if __name__ == "__main__":
    print_user_table_info()
    test_add_user()
    test_find_user_by()
    test_update_user()
    test_hash_password()
    test_register_user()
