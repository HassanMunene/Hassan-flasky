from flask import session, render_template, url_for, redirect, current_app, flash, abort, request
from . import main
from ..models import User, Role, Permission, Post
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from flask_login import current_user, login_required
from .. import db
from ..decorators import admin_required

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    This view function will handle the root route
    for the app.
    """
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post()
        post.body = form.body.data
        post.author = current_user._get_current_object()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))

    items_per_page = 15
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=items_per_page, error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)

@main.route('/user/<username>', methods=['GET'])
def user(username):
    """
    this view func will handle the route to see a specific
    user page eg http://<host>/user/john
    it will show the profile page
    it will also show the posts made by the user.
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    handle the process of users editing their profiles
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    """
    the view function that will handle the process of admins
    editing the profiles of users
    """
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/post/<int:id>')
def post(id):
    """
    This route will handle a specific url of a post.
    Basically in our app each post will have a specific
    unique url based on its id
    """
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])
