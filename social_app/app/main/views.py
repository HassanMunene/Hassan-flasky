from flask import session, render_template, url_for, redirect, current_app
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    This view function will handle the root route
    for the app.
    """
    return render_template('index.html')
