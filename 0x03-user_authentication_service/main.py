#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

# Testing User model
print(User.__tablename__)
for column in User.__table__.columns:
    print(f"{column}: {column.type}")

# Testing add_user method
my_db = DB()
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)
user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)

# Testing find_user_by method
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

# Testing update_user method
email = 'test@test.com'
hashed_password = "hashedPwd"
user = my_db.add_user(email, hashed_password)
print(user.id)
try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
except ValueError:
    print("Error")

# Create an Auth instance
auth = Auth()

# Testing _hash_password method
print(auth._hash_password("Hello Holberton"))

# Testing Auth.register_user method
email = 'me@me.com'
password = 'mySecuredPwd'
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

# Testing Auth.valid_login method
email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth.register_user(email, password)
print(auth.valid_login(email, password))
print(auth.valid_login(email, "WrongPwd"))
print(auth.valid_login("unknown@email", password))

# Testing Auth.create_session method
email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth.register_user(email, password)
print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))

# Testing Auth.get_user_from_session_id method
session_id = auth.create_session(email)
user = auth.get_user_from_session_id(session_id)
print(user.email if user else "No user found")

# Testing Auth.destroy_session method
auth.destroy_session(user.id)
user = auth.get_user_from_session_id(session_id)
print("Session destroyed" if user is None else "Session not destroyed")

# Testing Auth.get_reset_password_token method
email = 'me@me.com'
reset_token = auth.get_reset_password_token(email)
print(f"Reset token for {email}: {reset_token}")

# Testing Auth.update_password method
try:
    auth.update_password(reset_token, 'NewSecurePwd')
    print("Password updated successfully")
except ValueError as err:
    print(f"Error: {err}")

# Verify password update
print(auth.valid_login(email, 'NewSecurePwd'))
print(auth.valid_login(email, 'mySecuredPwd'))
