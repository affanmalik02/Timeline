from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfileForm, UpdateProfilePicForm
from ..models import User
import base64,io

users = Blueprint("users", __name__)

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ User Management views ************ """

# DONE
# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))

    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user.save()
            return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

# DONE
# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('users.account', username=user.username)) #""", image=update_profile_pic_form.picture.data"""
            else:
                flash('Login failed. Try again', 'failure')
    return render_template("login.html", form=form)

# DONE
# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('movies.index'))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_form = UpdateProfileForm()
    update_profile_pic_form = UpdateProfilePicForm()

    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            current_user.modify(username=update_username_form.username.data)
            current_user.save()

            return redirect(url_for('users.account')) #""", image=update_profile_pic_form.picture.data"""

        if update_profile_form.submit_profile.data and update_profile_form.validate():
            if update_profile_form.name.data:
                current_user.modify(name=update_profile_form.name.data)
            if update_profile_form.bio.data:
                current_user.modify(bio=update_profile_form.bio.data)
            if update_profile_form.location.data:
                current_user.modify(location=update_profile_form.location.data)
            current_user.save()

            return redirect(url_for('users.account'))

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            # TODO: handle update profile pic form submit
            image = update_profile_pic_form.picture.data
            filename = secure_filename(image.filename)
            content_type = f'images/{filename[-3:]}'

            if current_user.profile_pic:
                current_user.profile_pic.replace(image.stream, content_type=content_type)
            else:
                current_user.profile_pic.put(image.stream, content_type=content_type)
            
            current_user.save()

            return redirect(url_for('users.account')) #""", image=update_profile_pic_form.picture.data"""

    # TODO: handle get requests
    img = None
    if current_user.profile_pic != None:
        img = get_b64_img(current_user.username)

    url = url_for('movies.user_detail', username=current_user.username, image=img)

    user = User.objects(username=current_user.username).first()
    img = get_b64_img(user.username)

    return render_template(
        "account.html",
        user=user,
        update_username_form=update_username_form,
        update_profile_form=update_profile_form,
        update_profile_picture_form=update_profile_pic_form,
        greeting=f"Hello there, {current_user.username}!",
        reviews_url=url,
        image=img
    )