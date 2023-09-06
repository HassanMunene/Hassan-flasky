from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    """
    Role model will be mapped onto the
    roles table by the ORM in the specified database
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

class User(db.Model):
    """
    User model will be mapped onto the
    users table by the orm in the database specified
    by 'FLASKY_CONFIG'
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        """
        this is the getter method for the class
        attribute password, whenever you want to access
        the property this method is always called
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        This is the method that is usually called when you want
        to set a value to the attribute password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        This will verify the password entered by a user aginst
        the stored password_hash using the a specified method from
        werkzeug.security module
        """
        return check_password_hash(self.password_hash, password)
