from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown

# create extension instances but we will not initialize them because we
# do not have an instance of our application
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
pagedown = PageDown()

# This next section we will define the factory function that will create the instance of the application
# based on the configuration we want it to be in could be production, development or testing
def create_app(config_name):
    """
    this is the factory where all the cooking will happen
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # this kasmall section is for registering blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth_bp import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    return app
