import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

app = Flask(__name__)

# This section below is configuring the application with different settings
# such as sqlalchemy connections and email connections
app.config['SECRET_KEY'] = 'my sectret boy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://hassan:munene14347@localhost/flasky'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'awanzihassan@gmail.com'
app.config['MAIL_PASSWORD'] = 'xuhhwjkcsscxdmms'
app.config['MAIL_SUBJECT'] = '[Flasky]'
app.config['MAIL_SENDER'] = 'Flasky Admin <awanzihassan@gmail.com>'
app.config['FLASKY_ADMIN'] = 'sultanhamud081@gmail.com'

# This section below is to initialize the various extensions thats my application will use
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# The section we are defining database models that will be mapped into tables in mysql server
class Role(db.Model):
    """
    will be mapped to roles table
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        """
        string representation of roles
        """
        return '<Role {}>'.format(self.name)

class User(db.Model):
    """
    will be mapped into users table
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        """
        string rep of the object
        """
        return '<User {}>'.format(self.username)

# This next section we will be defining the form classes that will be used for input
class NameForm(FlaskForm):
    """
    will be rendered to be a form for user name input and submission button
    """
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField('Submit')

# This section we will define a function called send_email that will be used to send emails
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT'] + subject, sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)

# Here we are defining the objects that will be automatically available to our shell when we load the flask shell
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'mail': Mail
    }

# In this next section we are defining the routes that our application will use
@app.errorhandler(404)
def page_not_found(e):
    """
    handle 404 error status code
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """
    handler error from the server
    """
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    handle the root route of the app
    """
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)

        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))
