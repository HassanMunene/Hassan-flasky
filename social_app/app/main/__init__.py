"""
This will be the blueprint manufacturer or let's
just say we will make this package a blueprint by using
the Blueprint class from flask and we will in the process define the
name of the blueprint and the location in which the blueprint is defined
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
