from flask import current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous.serializer import Serializer

class Role(db.Model):
    """
    Role model will be mapped onto the
    roles table by the ORM in the specified database
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

class User(UserMixin, db.Model):
    """
    User model will be mapped onto the
    users table by the orm in the database specified
    by 'FLASKY_CONFIG'
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
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

    def generate_email_confirm_token(self):
        """
        This class method will be used sign the the user_id which in our
        case is and return the signed token as a string
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm_email(self, token):
        """
        This will take the signed token from the external source and then
        check if actually it is legit and can be loaded back to the content
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


@login_manager.user_loader
def load_user(user_id):
        """
        This method is method will be used to load a user
        from the db using the user_id
        """
        return User.query.get(int(user_id))
