from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import HiddenField, IntegerField, StringField, SubmitField, TextAreaField, PasswordField
from mongoengine import Document, StringField, EmailField, DateField, ImageField
from flask_login import UserMixin
from datetime import datetime

from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField, FileField
from wtforms.validators import Length, Optional

from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User

class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", 
        validators=[InputRequired(), Length(min=1, max=100)],
        render_kw={"placeholder": "Add to the timeline..."}
    )
    submit = SubmitField("Search")

class SharePostForm(FlaskForm):
    text = TextAreaField(
        "Comment", 
        validators=[InputRequired(), Length(min=1, max=250)],
        render_kw={"placeholder": "Add to the timeline..."}
    )
    submit = SubmitField("Share")

#FIX
class LikePostForm(FlaskForm):
    post_id = HiddenField('Post ID')
    submit_like = SubmitField("Like")

class DeletePostForm(FlaskForm):
    post_id = HiddenField('Post ID')
    submit_delete = SubmitField("Delete")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=20)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

# DONE
# TODO: implement fields
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# DONE
# TODO: implement
class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40, message="Username must be between 1 and 40 characters")])
    submit_username = SubmitField('Update Username') 

    # TODO: implement
    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")
        
class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=100), Optional()])
    bio = TextAreaField('Bio', validators=[Length(max=500), Optional()])
    location = StringField('Location', validators=[Length(max=50), Optional()])
    
    # Optional fields
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[Optional()])
    
    # Profile picture upload (optional)
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!'), Optional()])

    submit_profile = SubmitField('Update Profile')

# DONE
# TODO: implement
class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Profile Picture', validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg'])
    ])
    submit_picture = SubmitField('Upload')
