# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

# local
from .client import MovieClient  # Only needed if you're still using MovieClient

# update with your API Key (remove if no longer necessary)
OMDB_API_KEY = 'b3b0991b'

# do not remove these 2 lines (required for autograder to work)
if os.getenv('OMDB_API_KEY'):
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')

# Initialize extensions
db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()

# Initialize MovieClient if necessary (otherwise remove this)
movie_client = MovieClient(OMDB_API_KEY)

# Import blueprints
from .users.routes import users
from .posts.routes import posts  # Changed movies to posts

# Custom 404 error handler
def custom_404(e):
    return render_template("404.html"), 404

# Application factory function
def create_app(test_config=None):
    app = Flask(__name__)

    # Load configuration
    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)  # Changed movies to posts

    # Register custom error handlers
    app.register_error_handler(404, custom_404)

    # Set login view
    login_manager.login_view = "users.login"

    return app
