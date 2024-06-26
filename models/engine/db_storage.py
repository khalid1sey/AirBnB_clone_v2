#!/usr/bin/python3

"""This module defines the DBStorage"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from models.base_model import Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from custom_methods import CustomMethods


class DBStorage:
    """This class defines the database storage engine"""

    __engine = None
    __session = None
    __models = [State, City, User, Place, Review]

    def __init__(self):
        """Instantiates a new DBStorage object."""
        db_url = {
            "database": f"{getenv('HBNB_MYSQL_DB')}",
            "drivername": "mysql+mysqldb",
            "username": f"{getenv('HBNB_MYSQL_USER')}",
            "password": f"{getenv('HBNB_MYSQL_PWD')}",
            "host": f"{getenv('HBNB_MYSQL_HOST')}",
            "port": 3306,
            # Adjust the query parameters if necessary
            "query": {"charset": "utf8"}
        }
        self.__engine = create_engine(
            URL(**db_url),
            pool_pre_ping=True
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects in the current
        database session."""
        objects = {}

        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + "." + obj.id] = obj
        else:
            for model in self.__models:
                for obj in self.__session.query(model):
                    objects[obj.__class__.__name__ + "." + obj.id] = obj

        return objects

    def new(self, obj):
        """Adds the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and the current
        database session."""
        # set the default collation and character set
        # CustomMethods.set_default_collation(
        #     engine=self.__engine, db=getenv("HBNB_MYSQL_DB")
        # )

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )

        self.__session = scoped_session(session_factory)

    def rollback(self):
        """Rolls back the current database session."""
        self.__session.rollback()

    def close(self):
        """Closes the current session."""
        self.__session.remove()

    def drop_all(self):
        """Drops all tables in the database."""
        Base.metadata.drop_all(self.__engine)
