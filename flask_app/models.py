from flask_login import UserMixin
from datetime import datetime
from flask_wtf.file import FileField, FileRequired, FileAllowed
from . import db, login_manager

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

# DONE
# TODO: implement
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

# DONE
# TODO: implement fields
class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    
    joined_date = db.StringField()
    profile_pic = db.ImageField()       #fix
    
    name = db.StringField(min_length=1, max_length=100)
    bio = db.StringField(min_length=1, max_length=500)
    location = db.StringField(min_length=5, max_length=50)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

# DONE
# TODO: implement fields
class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(min_length=5, max_length=500, required=True)
    date = db.StringField(required=True)
    imdb_id = db.StringField(length=9, required=True)
    movie_title = db.StringField(min_length=1, max_length=100, required=True)
    image = db.StringField()
    likes = db.ListField(db.StringField())