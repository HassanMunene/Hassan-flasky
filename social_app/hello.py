from flask import Flask, render_template, session, redirect, url_for, flash
from flask-bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoo this is my secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymsql://hassan:munene14347@localhost/flasky'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

"""
Now In this next phase we will define the models that
will be used to represent the tables in the database
"""

class Role(db.Model):
    """
    This class will represent the roles table
    in the database
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        """
        will show the string representation of the object
        for debugging and logging purposes
        """
        return '<Role %r>' % self.name

class User(db.Model):
    """
    will be the table in the database called users
    """
    __tablename__ = users
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        """
        string rep of the object
        """
        return '<User %r>' %self.username

"""
This next part we will be defining the forms that we will
be using in our application
"""
class NameForm(FlaskForm):
    """
    This will be the form for someone to input their name
    """
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('submit')

"""
after we have defined the data models, the forms now is time to actually
define some route and view functions that will handle different routes
"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name buddy!")
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


