"""
This module will specifically handle the routes concerned
with authentication
"""
from flask import render_template, request, url_for, flash, redirect
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from flask_login import login_user, login_required, current_user, logout_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    will handle the /login route
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash("Invalid Email or Password")
    return render_template('auth/login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    log the user out
    """
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    This route will handle the process of regisration
    for user
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        flash('You can login now')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
