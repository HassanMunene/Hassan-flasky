import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Permission

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """
    avail all the object our flask shell will
    require instead of importing the all the time
    """
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'Permission': Permission
    }

@app.cli.command()
def test():
    """
    run the unit tests
    """
    import unittest
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(test)
