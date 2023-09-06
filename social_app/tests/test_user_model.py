"""
In this module and specifically the section below we are
testing the functionality of password hashing in our User model
"""
import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    """
    This is where all the cooking will happen
    """
    def test_password_setter(self):
        """
        Here we are testing whether actually when we set a value to the
        password property, hashing happens and that the hash value is stored
        in the password_hash attribute or column whatever you wanna call it
        """
        u = User()
        u.password = 'cat'
        self.assertTrue(u.password_hash is not None)

    def test_no_password_gettet(self):
        """
        Here we are testing that when we try to access the value
        of the password property the getter method raises an attribute error
        so we cannot access it
        """
        u = User()
        u.password = 'cat'
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        """
        Here we are testing if actually when user inputs a value
        it can be verified against the password_hash stored in db
        using the check_password_hash from security module of werkzeug
        """
        u = User()
        u.password = 'cat'
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salt_are_random(self):
        """
        Here we will test whether the salting done to our password
        is random when hashing. salting ensures that when two similar values are
        hashed they produce a different hash value
        """
        u1 = User()
        u2 = User()
        u1.password = 'cat'
        u2.password = 'cat'
        self.assertTrue(u1.password_hash != u2.password_hash)
