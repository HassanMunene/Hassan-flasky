from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

# create extension instances but we will not initialize them because we
# do not have an instance of our application
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

# This next section we will define the factory function that will create the instance of the application
# based on the configuration we want it to be in could be production, development or testing
def create_app(config_name):
    """
    this is the factory where all the cooking will happen
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    return app
