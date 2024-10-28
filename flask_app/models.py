from flask_login import UserMixin
from datetime import datetime
from flask_wtf.file import FileField, FileRequired, FileAllowed
from . import db, login_manager
from mongoengine import Document, StringField, EmailField, DateTimeField, ImageField, DateField, BooleanField
from flask_login import UserMixin
from datetime import datetime
import pytz


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    joined_date = db.DateField(default=lambda: datetime.now(pytz.timezone('US/Eastern')).date())
    profile_pic = db.ImageField()
    name = db.StringField(min_length=1, max_length=50)
    bio = db.StringField(min_length=1, max_length=250)
    location = db.StringField(min_length=5, max_length=50)
    birthday = DateField()

    followers = db.ListField(db.ReferenceField('User'))
    following = db.ListField(db.ReferenceField('User'))

    # Returns unique string identifying our object
    def get_id(self):
        return self.username
    
    def follow(self, user):
        if user not in self.following:
            self.following.append(user)
            user.followers.append(self)
            self.save()
            user.save()

    def unfollow(self, user):
        if user in self.following:
            self.following.remove(user)
            user.followers.remove(self)
            self.save()
            user.save()

    def is_following(self, user):
        return user in self.following

    def is_followed_by(self, user):
        return user in self.followers

class Post(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(min_length=1, max_length=250, required=True)
    date = db.DateTimeField(default=lambda: datetime.now(pytz.timezone('US/Eastern')), required=True)
    image = db.StringField()
    likes = db.ListField(db.StringField())
    post_id = db.StringField()