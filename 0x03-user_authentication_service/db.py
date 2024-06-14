#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class"""
    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by keyword arguments"""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the given attributes")
        except MultipleResultsFound:
            raise InvalidRequestError("Multiple users found with the given attributes")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid request arguments")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes"""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User not found")
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Attribute {key} does not exist on User")
            setattr(user, key, value)
        self._session.commit()
