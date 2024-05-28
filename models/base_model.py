#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time_format = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    else:
        id = None
        created_at = None
        updated_at = None

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if isinstance(self.created_at, str):
                self.created_at = datetime.strptime(self.created_at, time_format)
            elif not self.created_at:
                self.created_at = datetime.utcnow()
            
            if isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(self.updated_at, time_format)
            elif not self.updated_at:
                self.updated_at = datetime.utcnow()
            
            if not self.id:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        new_dict["created_at"] = new_dict["created_at"].strftime(time_format)
        new_dict["updated_at"] = new_dict["updated_at"].strftime(time_format)
        new_dict["__class__"] = self.__class__.__name__
        new_dict.pop("_sa_instance_state", None)
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
