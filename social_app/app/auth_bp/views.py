"""
This module will specifically handle the routes concerned
with authentication
"""
from flask import render_template, request, url_for, flash, redirect
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from ..emails import send_email
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
        token = user.generate_email_confirm_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    Will be used to confirm the email.For email validation
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_email(token):
        db.session.commit()
        flash("Your account has been confirmed. Thanks!")
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))
