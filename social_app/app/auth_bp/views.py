"""
This module will specifically handle the routes concerned
with authentication
"""
from flask import render_template
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    will handle the /login route
    """
    return render_template('auth/login.html')
