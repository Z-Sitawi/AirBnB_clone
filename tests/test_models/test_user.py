#!/usr/bin/python3
"""This module serves as a unittest suite for the User class.
The tests cover a range of scenarios, including the initialization,
string representation, saving, and dictionary conversion of User objects.
"""
import unittest
import os
import datetime
from models.user import User
from models.base_model import BaseModel
import models
from time import sleep
import json


class TestUserInit(unittest.TestCase):
    """Test cases for the initialization of the User class.
    """
    def setUp(self):
        """Rename the storage file, so it doesn't get overwrited

        Returns:
            The default behavior of the parent class
        """
        try:
            os.rename('file.json', 'temp')
        except FileNotFoundError:
            pass

        return super().setUp()

    def tearDown(self):
        """Reset the storage file name to its default

        Returns:
            The default behavior of the parent class
        """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

        try:
            os.rename('temp', 'file.json')
        except FileNotFoundError:
            pass

        return super().tearDown()

    def test_parent_class_is_BaseModel(self):
        """Test if the parent of the User class is BaseModel
        """
        self.assertIsInstance(User(), BaseModel)
        self.assertTrue(issubclass(User, BaseModel))

    def test_public_attributes(self):
        """Test the types of public attributes.
        """
        obj = User()
        self.assertEqual(str, type(obj.id))
        self.assertEqual(datetime.datetime, type(obj.created_at))
        self.assertEqual(datetime.datetime, type(obj.updated_at))
        self.assertEqual(str, type(obj.email))
        self.assertEqual(str, type(obj.password))
        self.assertEqual(str, type(obj.first_name))
        self.assertEqual(str, type(obj.last_name))

    def test_empty_user_attributes(self):
        """Test empty user attribute values.
        """
        obj = User()
        self.assertEqual(obj.email, "")
        self.assertEqual(obj.password, "")
        self.assertEqual(obj.first_name, "")
        self.assertEqual(obj.email, "")

    def test_email_if_it_actually_email(self):
        """Test if the email attribute follows the email pattern.
        """
        obj = User()
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        obj.email = "abdo@gmail.com"
        self.assertRegex(obj.email, regex)
        obj.email = "abdo@home"
        self.assertNotRegex(obj.email, regex)

    def test_uniq_id_for_multiple_objects(self):
        """Test uniqueness of IDs for multiple objects.
        """
        obj1 = User()
        obj2 = User()
        obj3 = User()
        obj4 = User()
        ids = {obj1.id, obj2.id, obj3.id, obj4.id}
        self.assertTrue(len(ids) == 4)

    def test_same_createdAt_updatedAt(self):
        """Test if created_at and updated_at are the same initially.
        """
        obj = User()
        self.assertEqual(obj.created_at, obj.updated_at)

    def test_obj_existance_in_storage(self):
        """Test if the object exists in the storage.
        """
        obj = User()
        self.assertIn(obj, models.storage.all().values())

    def test_instance_recreate_from_dict(self):
        """Test recreating an instance from a dictionary.
        """
        date = datetime.datetime(2024, 1, 14, 17, 7, 0, 0).isoformat()
        dict1 = {
            'id': '1809',
            'created_at': date,
            'updated_at': date,
            '__class__': 'User',
            'email': 'abdo@gmail.com',
            'password': 'abdo@alx',
            'first_name': 'Abdelrahman',
            'last_name': 'Mohamed'
            }
        obj = User(**dict1)
        dict2 = obj.to_dict()
        self.assertDictEqual(dict1, dict2)

    def test_unused_args(self):
        """Test handling unused positional arguments.
        """
        obj = User('1809')
        self.assertNotIn('1809', obj.__dict__.values())

    def test_unused_args_and_used_kwargs(self):
        """Test handling unused positional arguments and
        used keyword arguments.
        """
        obj = User('1809', year='2024')
        self.assertNotIn('1809', obj.__dict__.values())
        self.assertIn('2024', obj.__dict__.values())

    def test_adding_additional_attributes(self):
        """Test adding additional attributes to the object.
        """
        obj = User()
        obj.name = 'Abdelrahman'
        obj.code = 7
        obj.team = ['Zakaria', 'Abdelrahman']
        obj.project = {'AirBnB': 'team_project'}
        obj.rate = 99.6
        obj.available = True

        self.assertEqual(obj.name, 'Abdelrahman')
        self.assertEqual(obj.code, 7)
        self.assertEqual(obj.team, ['Zakaria', 'Abdelrahman'])
        self.assertEqual(obj.project, {'AirBnB': 'team_project'})
        self.assertEqual(obj.rate, 99.6)
        self.assertEqual(obj.available, True)

    def test_createdAt_typeError(self):
        """Test raising a ValueError if created_at has an invalid type
        """
        dict1 = {
            'id': '1809',
            'created_at': '1809',
            'updated_at': '2002',
            '__class__': 'User',
            'email': 'abdo@gmail.com',
            'password': 'abdo@alx',
            'first_name': 'Abdelrahman',
            'last_name': 'Mohamed'
            }
        with self.assertRaises(ValueError):
            User(**dict1)

    def test_updatedAt_typeError(self):
        """Test raising a ValueError if updated_at has an invalid type.
        """
        date = datetime.datetime(2024, 1, 14, 17, 7, 0, 0)
        dict1 = {
            'id': '1809',
            'created_at': date.isoformat(),
            'updated_at': '2002',
            '__class__': 'User',
            'email': 'abdo@gmail.com',
            'password': 'abdo@alx',
            'first_name': 'Abdelrahman',
            'last_name': 'Mohamed'
            }
        with self.assertRaises(ValueError):
            User(**dict1)

    def test_with_None_kwargs(self):
        """Test raising a TypeError if any keyword argument is None.
        """
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserStr(unittest.TestCase):
    """Test cases for the __str__ method of the User class.
    """
    def setUp(self):
        """Rename the storage file, so it doesn't get overwrited

        Returns:
            The default behavior of the parent class
        """
        try:
            os.rename('file.json', 'temp')
        except FileNotFoundError:
            pass

        return super().setUp()

    def tearDown(self):
        """Reset the storage file name to its default

        Returns:
            The default behavior of the parent class
        """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

        try:
            os.rename('temp', 'file.json')
        except FileNotFoundError:
            pass

        return super().tearDown()

    def test_formated_output(self):
        """ Test the formatted string output of the User object.
        """
        obj = User()
        obj.id = '1809'
        obj.created_at = datetime.datetime(2024, 1, 14, 19, 45, 3, 255968)
        obj.updated_at = obj.created_at
        obj.email = 'abdo@email.com'
        obj.password = 'abdo1234'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'

        result = "[User] (1809) {'id': '1809', 'created_at':" + \
            " datetime.datetime(2024, 1, 14, 19, 45, 3, 255968)," + \
            " 'updated_at': datetime.datetime(2024, 1, 14, 19, 45," + \
            " 3, 255968), 'email': 'abdo@email.com', 'password': " + \
            "'abdo1234', 'first_name': 'Abdelrahman', 'last_name': 'Mohamed'}"

        self.assertEqual(str(obj), result)


class TestUserSave(unittest.TestCase):
    """Test cases for the save method of the User class.
    """
    def setUp(self):
        """Rename the storage file, so it doesn't get overwrited

        Returns:
            The default behavior of the parent class
        """
        try:
            os.rename('file.json', 'temp')
        except FileNotFoundError:
            pass

        return super().setUp()

    def tearDown(self):
        """Reset the storage file name to its default

        Returns:
            The default behavior of the parent class
        """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

        try:
            os.rename('temp', 'file.json')
        except FileNotFoundError:
            pass

        return super().tearDown()

    def test_save_with_args(self):
        """Test raising a TypeError when save method is called
        with arguments.
        """
        obj = User()
        obj.email = 'abdo@email.com'
        obj.password = 'abdo123'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'
        with self.assertRaises(TypeError):
            obj.save('arg')

    def test_updatedAt_greaterThan_createdAt(self):
        """Test if updated_at is greater than created_at after saving.
        """
        obj = User()
        obj.email = 'abdo@email.com'
        obj.password = 'abdo123'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'
        sleep(0.3)
        obj.save()
        self.assertGreater(obj.updated_at, obj.created_at)

    def test_updatedAt_greaterThan_prev_updatedAt(self):
        """Test if updated_at is greater than the previous
        updated_at after saving.
        """
        obj = User()
        obj.email = 'abdo@email.com'
        obj.password = 'abdo123'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'
        prev_updated = obj.updated_at
        obj.save()
        self.assertGreater(obj.updated_at, prev_updated)

    def test_updatedAt_type(self):
        """Test if updated_at is a datetime object after saving.
        """
        obj = User()
        obj.email = 'abdo@email.com'
        obj.password = 'abdo123'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'
        obj.updated_at = 'foo'
        obj.save()
        self.assertEqual(datetime.datetime, type(obj.updated_at))

    def test_saved_obj_in_storage(self):
        """Test if the saved object is present in the storage.
        """
        obj = User()
        obj.email = 'abdo@email.com'
        obj.password = 'abdo123'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'
        obj.save()
        with open('file.json', 'r') as f:
            instances = json.load(f)
        self.assertIn(obj.to_dict(), list(instances.values()))


class TestUserToDict(unittest.TestCase):
    """Test cases for the to_dict method of the User class.
    """
    def setUp(self):
        """Rename the storage file, so it doesn't get overwrited

        Returns:
            The default behavior of the parent class
        """
        try:
            os.rename('file.json', 'temp')
        except FileNotFoundError:
            pass

        return super().setUp()

    def tearDown(self):
        """Reset the storage file name to its default

        Returns:
            The default behavior of the parent class
        """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

        try:
            os.rename('temp', 'file.json')
        except FileNotFoundError:
            pass

        return super().tearDown()

    def test_to_dict_with_args(self):
        """Test raising a TypeError when to_dict method is
        called with arguments.
        """
        obj = User()
        with self.assertRaises(TypeError):
            obj.to_dict('arg')

    def test_create_instance_from_dict(self):
        """Test creating an instance from a dictionary.
        """
        obj = User()
        data = obj.to_dict()
        obj2 = User(**data)
        self.assertEqual(obj.id, obj2.id)
        self.assertEqual(obj.created_at, obj2.created_at)
        self.assertEqual(obj.updated_at, obj2.updated_at)

    def test_return_type(self):
        """Test if the return type of to_dict is a dictionary.
        """
        obj = User()
        obj.email = 'abdo@email.com'
        obj.password = 'abdo123'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'
        data = obj.to_dict()
        self.assertEqual(dict, type(data))

    def test_dict_keys_types(self):
        """Test if the keys in the dictionary are of type string.
        """
        obj = User()
        obj.email = 'abdo@email.com'
        obj.password = 'abdo123'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'
        data = obj.to_dict()
        for key in data.keys():
            self.assertEqual(str, type(key))

    def test_dict_keys(self):
        """Test if the keys in the dictionary match the expected keys.
        """
        obj = User()
        obj.email = 'abdo@email.com'
        obj.password = 'abdo123'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'
        data = list(obj.to_dict().keys())
        keys = [
            'id', 'created_at', 'updated_at',
            '__class__', 'email', 'password',
            'first_name', 'last_name'
            ]
        keys.sort()
        data.sort()
        self.assertEqual(data, keys)

    def test_dict_values_types(self):
        """Test if the values in the dictionary are of type string.
        """
        obj = User()
        obj.email = 'abdo@email.com'
        obj.password = 'abdo123'
        obj.first_name = 'Abdelrahman'
        obj.last_name = 'Mohamed'
        data = obj.to_dict()
        for value in data.values():
            self.assertEqual(str, type(value))

    def test_dict_values(self):
        """Test if the values in the dictionary match the
        expected values.
        """
        date = datetime.datetime(2024, 1, 14, 17, 7, 0, 0)
        dict1 = {
            'id': '1809',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
            '__class__': 'User',
            'email': 'abdo@email.com',
            'password': 'abdo123',
            'first_name': 'Abdelrahman',
            'last_name': 'Mohamed'
            }

        obj = User(**dict1)
        for key, value in obj.to_dict().items():
            self.assertEqual(dict1[key], value)


if __name__ == '__main__':
    unittest.main()
