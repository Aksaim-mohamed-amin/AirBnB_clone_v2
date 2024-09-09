#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects

        cls_dict = {}
        for key, obj in self.__objects.items():
            if key.split('.')[0] == cls.__name__:
                cls_dict[key] = obj.to_dict()
        return cls_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects.update({obj.__class__.__name__ + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            for key, obj in FileStorage.__objects.items():
                temp[key] = obj.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def delete(self, obj=None):
        """Delete obj from __objects"""
        if obj is None:
            return

        key = f"{obj.__class__.__name__}.{obj.id}"
        del (FileStorage.__objects[key])
