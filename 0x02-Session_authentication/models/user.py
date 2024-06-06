#!/usr/bin/env python3
""" User module """

from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker, relationship
from models.base import Base
import hashlib


class User(Base):
    """ User class """

    __tablename__ = 'users'

    email = Column(String(128), nullable=False, unique=True)
    _password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """ Getter of the password """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """ Setter of a new password: encrypt in SHA256 """
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate a password """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """ Display User name based on email/first_name/last_name """
        if self.email is None and self.first_name is None and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def search(cls, search_criteria: dict):
        """
        Search for a user based on search criteria.
        Example: User.search({"email": "user@example.com"})
        """
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import create_engine

        engine = create_engine(
            'postgresql://username:password@localhost/mydatabase'
        )
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            users = session.query(User).filter_by(**search_criteria).all()
            return users
        except Exception as e:
            print(f"Error searching for user: {e}")
            return []
        finally:
            session.close()
