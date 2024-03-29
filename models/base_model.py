#!/usr/bin/python3
"""Base class for all models"""
import uuid
import datetime
import models


class BaseModel():
    """BaseModel
    desc:
        Contains all the necassary and shared attributes/methods.
    """

    def __init__(self, *args, **kwargs):
        """Constructor for the BaseModel class
        desc:
            Initialize all the mandatory attributes.
        """

        if len(kwargs) != 0:
            self.create(**kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def create(self, **dictionary):
        """Update the class Base and returns a instance with all
            attributes already set
        Args:
            dictionary: Dictionary with all attributes of the object
        Return:
            An instance with all attributes already set
        """
        for key, value in dictionary.items():
            if key == '__class__':
                continue
            elif key == 'created_at':
                value = datetime.datetime.fromisoformat(
                    dictionary['created_at']
                    )
            elif key == 'updated_at':
                value = datetime.datetime.fromisoformat(
                    dictionary['updated_at']
                    )

            setattr(self, key, value)

    def __str__(self):
        """Convert the instance to string.

        Returns:
            Human readable representation of the class.
        """

        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update the updated_at instance attribute."""

        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """Convert the instance to its dictionary representation

        Returns:
            All the instance attributes in a dictionary
        """

        instance_to_dict = self.__dict__.copy()
        instance_to_dict.update({
            '__class__': self.__class__.__name__,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
            })
        return instance_to_dict
