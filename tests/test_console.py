#!/usr/bin/python3

"""This module tests the console."""

import os
import unittest
from unittest.mock import patch
from io import StringIO
import sqlalchemy
from console import HBNBCommand
from custom_methods import CustomMethods
import models

instance = CustomMethods()


class TestConsole(unittest.TestCase):
    """Tests the console."""

    def setUp(self):
        self.cli = HBNBCommand()

        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            models.storage.rollback()

    def test_do_create_no_args(self):
        """Test `create` with no model name."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.cli.onecmd("create")
            self.assertEqual(f.getvalue(), "** class name missing **\n")

    def test_do_create_invalid_class(self):
        """Test `create` with an invalid model name."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.cli.onecmd("create MyClass")
            self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "file")
    def test_do_create_valid_class(self):
        """Test `create` with a valid model name."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.cli.onecmd("create BaseModel")
            self.assertNotEqual(f.getvalue(), "** class doesn't exist **\n")
            self.assertNotEqual(f.getvalue(), "** class name missing **\n")

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "file")
    def test_do_create_one_attribute(self):
        """Test `create` with one attribute."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.cli.onecmd('create BaseModel name="Orton"')

            key = instance.retrieve_key("BaseModel", instance.retrieve_uuid(f))
            obj = models.storage.all()[key]
            self.assertTrue(
                set({"name": "Orton"}.items()).issubset(
                    obj.__dict__.items()
                )
            )

    def test_do_create_escaped_str(self):
        """Test `create` with an escaped string attribute value."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.cli.onecmd(
                'create User first_name=""Randy"_Orton" '
                'email="randyorton@gmail.com" password="xyz246"'
            )

            key = instance.retrieve_key("User", instance.retrieve_uuid(f))
            obj = models.storage.all()[key]
            self.assertTrue(
                set(
                    {
                        "first_name": '"Randy" Orton',
                        "email": "randyorton@gmail.com",
                        "password": "xyz246",
                    }.items()
                ).issubset(obj.__dict__.items()),
            )

    def test_do_create_multiple_attributes(self):
        """Test `create` with multiple attributes."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.cli.onecmd(
                'create User first_name="Randy" last_name="Orton" '
                'email="randyorton@gmail.com" password="xyz246"'
            )

            key = instance.retrieve_key("User", instance.retrieve_uuid(f))
            obj = models.storage.all()[key]
            self.assertTrue(
                set(
                    {
                        "first_name": "Randy",
                        "last_name": "Orton",
                        "email": "randyorton@gmail.com",
                        "password": "xyz246",
                    }.items()
                ).issubset(obj.__dict__.items()),
            )

    def test_do_create_invalid_attribute(self):
        """Test `create` with an invalid attribute."""
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            print("Using DB")
            with self.assertRaises(sqlalchemy.exc.IntegrityError):
                self.cli.onecmd(
                    'create User invalid_attribute="Randy Orton"'
                )
        else:
            print("Using File storage")
            with patch("sys.stdout", new=StringIO()) as f:
                self.cli.onecmd(
                    'create User invalid_attribute="Randy Orton"'
                )

                key = instance.retrieve_key("User", instance.retrieve_uuid(f))
                obj = models.storage.all()[key]
                self.assertNotIn("invalid_attribute", obj.__dict__)


if __name__ == "__main__":
    unittest.main()
