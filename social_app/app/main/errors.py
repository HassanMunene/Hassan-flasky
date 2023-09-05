"""
here our main purpose is to handle errors and in this case
we will use the decorator .app_errorhandler instead of .errorhandler
this is because we want the errors to be handled globally and not to
be tied to a specific blueprint. May in the future we could handle the errors
specifically for each blueprint
"""
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    """
    this beautiful function will handle
    situaions where the resource being searched is not found
    """
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    """
    this fun will tell us when we have an error
    in our app and therefore the server cannot handle it
    """
    return render_template('500.html'), 500
