from . import db

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
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


