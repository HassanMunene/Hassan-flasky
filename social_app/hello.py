from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my sectret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://hassan:munene14347@localhost/flasky'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class Role(db.Model):
    """
    the model that will map into roles table
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.Relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        """
        string representation of the object
        """
        return '<Role %r>' %self.name

class User(db.Model):
    """
    The model that will map into the users table
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        """
        string representation of the object
        """
        return '<User %r>' %self.username

"""
This is the sections where we define the forms that we will be using now
"""
class NameForm(FlaskForm):
    """
    the form for inserting the name
    """
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


"""
In this sections we will use the shell context processor to automatically add some objects
to our flask shell instead of manually importing them all the time
"""
@app.shell_context_processor
def make_shell_context():
    """
    return a dctionary of the objects you want to be
    automatically loaded
    """
    return {
        'database': db,
        'User': User,
        'Role': Role,
    }
"""
Now here lets define the routes for our small application
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
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known'))

