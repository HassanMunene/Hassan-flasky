from flask import session, render_template, url_for, redirect, current_app
from . import main
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    This view function will handle the root route
    for the app.
    """
    return render_template('index.html')

@main.route('/user/<username>', methods=['GET'])
def user(username):
    """
    this view func will handle the route to see a specific
    user page eg http://<host>/user/john
    """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
