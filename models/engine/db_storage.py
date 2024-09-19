#!/usr/bin/python3
"""Define a new"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Define the db storage class"""
    __engine = None
    __session = None

    classes = {
        'User': User, 'State': State, 'City': City,
        'Amenity': Amenity, 'Place': Place, 'Review': Review
    }

    def __init__(self):
        """Initialize a new DBStoorage instance"""
        mysql_user = os.getenv('HBNB_MYSQL_USER')
        mysql_pass = os.getenv('HBNB_MYSQL_PWD')
        mysql_host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        mysql_db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(mysql_user, mysql_pass,
                                              mysql_host, mysql_db),
                                      pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Qurey on the current database session all objects
        depending on the class name
        """
        cls_dict = {}

        if not isinstance(cls, str):
            cls = cls.__name__

        if cls:
            objects = self.__session.query(self.classes[cls]).all()
            for obj in objects:
                key = f"{obj.__class__.__name__}.{obj.id}"
                cls_dict[key] = obj
        else:
            for model_name, model_class in self.classes.items():
                objects = self.__session.query(model_class).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    cls_dict[key] = obj

        return (cls_dict)

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create a session adand reload the database"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """
        call remove() method on the private session attribute
        """
        if self.__session:
            self.__session.close()
