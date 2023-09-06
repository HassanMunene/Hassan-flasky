import unittest
from flask import current_app
from app import create_app, db

class BasicTestCase(unittest.TestCase):
    """
    test where the current_app is actually existing
    and test where the configurations for testing are actually set up
    """
    def setUp(self):
        """
        create an environment for each test that
        imitates the actual running application
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        clean up the environment for each test
        after the test has completed
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_is_existing(self):
        """
        testing if the current_app object
        actually shows that there is a current app
        """
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """
        test that actually the configuration for testing
        is actually running
        """
        self.assertTrue(current_app.config['TESTING'])
