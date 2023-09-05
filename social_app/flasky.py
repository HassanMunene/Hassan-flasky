import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role

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
        'Role': Role
    }
