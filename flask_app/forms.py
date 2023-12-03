from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import HiddenField, IntegerField, StringField, SubmitField, TextAreaField, PasswordField
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

class MovieReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", 
        validators=[InputRequired(), Length(min=5, max=500)],
        render_kw={"placeholder": "Add to the timeline..."}
    )
    submit = SubmitField("Share")

#FIX
class LikePostForm(FlaskForm):
    review_id = HiddenField('Review ID')
    submit_like = SubmitField("Like")

class DeletePostForm(FlaskForm):
    review_id = HiddenField('Review ID')
    submit_delete = SubmitField("Delete")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
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
    name = StringField('Name', validators=[Length(max=50, message="Enter a valid name")])
    submit_name = SubmitField('Update Name')
    bio = TextAreaField('Bio', validators=[Length(max=500, message="Bio must be less than 250 characters")])
    submit_bio = SubmitField('Update Bio')
    location = StringField('Location', validators=[Length(max=50, message="Enter a valid location")])
    submit_location = SubmitField('Update Location') 
    
    submit_profile = SubmitField('Update Profile')

# DONE
# TODO: implement
class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Profile Picture', validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg'])
    ])
    submit_picture = SubmitField('Upload')
