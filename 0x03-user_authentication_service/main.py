#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

def print_user_table_info():
    print(User.__tablename__)

    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))

def test_add_user():
    my_db = DB()

    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(user_1.id)

    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(user_2.id)

def test_find_user_by():
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

if __name__ == "__main__":
    print_user_table_info()
    test_add_user()
    test_find_user_by()
