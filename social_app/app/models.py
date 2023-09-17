from flask import current_app, request
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous.serializer import Serializer
from datetime import datetime
import hashlib

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

#Role---------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
class Role(db.Model):
    """
    Role model will be mapped onto the
    roles table by the ORM in the specified database
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def has_permission(self, perm):
        """
        This func will perform the bitwise & operator
        to check if a certain permission is contained
        in the permissions attribute od Role
        will either return True or False
        """
        return self.permissions & perm == perm

    def add_permission(self, perm):
        """
        It will first check if the permissions attr has the specified
        perm if not then it will add the permission
        """
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        """
        This will remove the specified permission if the perm
        is found in the permissions attr
        """
        if self.has_permission(perm):
            self.permissions -= perm
    def reset_permission(self):
        """
        reset the permissions back to 0
        """
        self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

#--------------------------------------------------------------------------------------------------------------------------------------------
#User--------------------------------------------------------------------------------------------------------------------------------------------
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
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    avatar_hash = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
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

    def can(self, perm):
        """
        This will check whether a use has a certain permission
        """
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        """
        check whether a certain user is an admin by checking
        if they have the admin permission
        """
        return self.can(Permission.ADMIN)

    def ping(self):
        """
        This method will update the last seen time everytime a user
        accesses the application. so it keeps refreshing last_seen
        and to keep this method updating all the time we will use the
        before hook to call it from there
        """
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        """
        will generate some avator images for user profile using md5 hash
        """
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return f'{url}/{hash}?s={size}&d={default}&r={rating}'

#---------------------------------------------------------------------------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
        """
        This method is method will be used to load a user
        from the db using the user_id
        """
        return User.query.get(int(user_id))

#--------------------------------------------------------------------------------------------------------------------------------------------
class AnonymousUser(AnonymousUserMixin):
    """
    This class will provide functionality for users that
    have not yet been authenticated or rather logged in
    """
    def can(self, permission):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

#---------------------------------------------------------------------------------------------------------------------------------------------Blog post model
#--------------------------------------------------------------------------------------------------------------------------------------------
class Post(db.Model):
    """
    new database model for representing blog posts
    keep in mind that it has 1-many rel with users as they are the authors
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
