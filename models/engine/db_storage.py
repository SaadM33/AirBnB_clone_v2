#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """Database storage class for SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage."""

        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}.{password}@localhost/{db}",
            pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Reload objects from the database."""
        Base.metadata.create_all(self.__engine)

        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def new(self, obj):
        """Add object to the current database session."""
        if obj:
            self.__session.add(obj)

    def all(self, cls=None):
        """ Query all classes or specific one by ID"""
        objects = {}
        if cls:
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for cls in [User, State, City, Amenity, Place, Review]:
                query = self.__session.query(cls)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current database session."""
        if obj:
            self.__session.delete(obj)
