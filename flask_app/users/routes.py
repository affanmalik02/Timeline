from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfileForm, UpdateProfilePicForm, SearchForm    
from ..models import User
import base64,io
from ..utils import current_time

from flask import Flask
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'email@gmail.com'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_DEFAULT_SENDER'] = 'email@gmail.com'
mail_enabled = False    #set to true to enable mail

mail = Mail(app)

users = Blueprint("users", __name__)

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ User Management views ************ """

@users.context_processor
def context_processor():
    return {'search_form': SearchForm()}

# DONE
# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.timeline'))

    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            user = User(username=form.username.data, email=form.email.data, password=hashed_password, joined_date=datetime.now())

            user.save()
            
            if mail_enabled:
                msg = Message("Welcome to Timeline", recipients=[form.email.data])
                msg.body = "Thank you for signing up!"
                mail.send(msg)
            
            return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.timeline'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('posts.timeline', username=user.username))
            else:
                flash('Invalid username or password ', 'failure')
    return render_template("login.html", form=form)

# DONE
# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts.timeline'))

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
            if update_profile_form.birthday.data:
                current_user.modify(birthday=update_profile_form.birthday.data)
            
            current_user.save()

            return redirect(url_for('users.account'))

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
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

    url = url_for('posts.user_detail', username=current_user.username, image=img)

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

@users.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    user = User.objects(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('main.index'))
    
    if user != current_user:
        current_user.follow(user)
        flash(f"You are now following {user.username}.")
    else:
        flash("You cannot follow yourself.")

    return redirect(url_for('posts.user_detail', username=username))

@users.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user = User.objects(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('main.index'))

    if user != current_user:
        current_user.unfollow(user)
        flash(f"You have unfollowed {user.username}.")
    else:
        flash("You cannot unfollow yourself.")
    
    return redirect(url_for('posts.user_detail', username=username))

@users.route('/<username>/followers')
def followers(username):
    user = User.objects(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('main.index'))

    return render_template('followers.html', user=user, followers=user.followers, get_b64_img=get_b64_img)

@users.route('/<username>/following')
def following(username):
    user = User.objects(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for('main.index'))

    return render_template('following.html', user=user, following=user.following, get_b64_img=get_b64_img)
