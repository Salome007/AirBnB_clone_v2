#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """
    A base class for all hbnb models

    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            # remove unused __class__ key in kwarg
            try:
                del kwargs["__class__"]
            except KeyError as e:
                pass
            # format date
            # try:
            # kwargs["updated_at"] = datetime.strptime(
            #     kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"
            # )
            # kwargs["created_at"] = datetime.strptime(
            #     kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
            #     )
            # except KeyError as e:
            #     pass
            # set instance's attributes
            for key, value in kwargs.items():
                setattr(self, key, value)
            # update __dict__ to match the current values
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        kwarg = {"__class__": (str(type(self)).split(".")[-1]).split("'")[0]}
        dictionary.update(kwarg)
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        # remove _sa_instance_state in dict
        # dictionary.pop('_sa_instance_state', None)
        try:
            del dictionary["_sa_instance_state"]
        except KeyError as e:
            pass
        return dictionary

    def delete(self):
        """
        delete the current instance from the storage\
        (models.storage) by calling the method delete
        """
        from models import storage

        storage.delete(self)
