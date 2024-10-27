import base64, io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required, login_user, logout_user

from .. import movie_client  # You might want to rename this if no longer movie-related
from ..forms import SharePostForm, SearchForm
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..forms import LikePostForm, DeletePostForm
from ..models import User, Post  # Changed Review to Post
from ..utils import current_time
from datetime import datetime
from .. import bcrypt

posts = Blueprint("posts", __name__)

""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """

@posts.context_processor
def context_processor():
    return {'search_form': SearchForm()}

@posts.context_processor
def utility_processor():
    return dict(get_b64_img=get_b64_img)

@posts.route("/", methods=["GET", "POST"])
def timeline():
    search_form = SearchForm()
    post_form = SharePostForm()
    like_post_form = LikePostForm()
    delete_post_form = DeletePostForm()

    if search_form.validate_on_submit():
        return redirect(url_for("posts.query_results", query=search_form.search_query.data))

    if post_form.validate_on_submit():
        user = current_user._get_current_object()
        img = get_b64_img(user.username)

        post = Post(  # Changed Review to Post
            commenter=user,
            content=post_form.text.data,
            date=datetime.utcnow(),
            image=img,
            likes=[],
        )

        post.save()
        return redirect(url_for("posts.timeline"))

    if request.method == "POST":
        action = request.form.get('action')
        post_id = request.form.get('post_id')  # Changed review_id to post_id

        if action == 'Like' and like_post_form.validate():
            post = Post.objects(id=post_id).first()  # Changed Review to Post
            if post:
                current_user_username = current_user.get_id()
                if current_user_username in post.likes:
                    post.likes.remove(current_user_username)
                else:
                    post.likes.append(current_user_username)
                post.save()
        elif action == 'Delete' and delete_post_form.validate():
            post = Post.objects(id=post_id).first()  # Changed Review to Post
            if post and post.commenter.id == current_user.id:
                post.delete()

        return redirect(url_for("posts.timeline"))

    user_posts = Post.objects()  # Changed Review to Post
    
    return render_template(
        "timeline.html",  # Changed index.html to timeline.html
        search_form=search_form,
        post_form=post_form,
        user_posts=user_posts,
        like_post_form=like_post_form,
        delete_post_form=delete_post_form,
    )

@posts.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = User.objects(username=query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)

@posts.route("/posts/<post_id>", methods=["GET", "POST"])
def post_detail(post_id):
    try:
        result = movie_client.retrieve_movie_by_id(post_id)  # You might need to rename movie_client too
    except ValueError as e:
        return render_template("post_detail.html", error_msg=str(e))

    form = SharePostForm()
    
    if form.validate_on_submit():
        user = current_user._get_current_object()
        img = get_b64_img(user.username)

        post = Post(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            image=img,
            likes=[],
        )

        post.save()

        return redirect(request.path)

    user_posts = Post.objects()  # Changed Review to Post

    return render_template(
        "post_detail.html",  # Changed movie_detail.html to post_detail.html
        form=form, 
        post=result,  # Renamed movie to post
        user_posts=user_posts  # Renamed reviews to user_posts
    )

@posts.route("/user/<username>", methods=['GET', 'POST'])
def user_detail(username):
    user = User.objects(username=username).first()

    if user is None:
        return render_template("user_detail.html", error="User not found", image=None)
    
    user_posts = Post.objects(commenter=user.id)  # Changed Review to Post
    img = get_b64_img(user.username)
    
    like_post_form = LikePostForm()
    delete_post_form = DeletePostForm()
    
    if request.method == 'POST':
        action = request.form.get('action')
        post_id = request.form.get('post_id')  # Changed review_id to post_id

        if action == 'Like' and like_post_form.validate():
            post = Post.objects(id=post_id).first()  # Changed Review to Post
            if post:
                current_user_username = current_user.get_id()
                if current_user_username in post.likes:
                    post.likes.remove(current_user_username)
                else:
                    post.likes.append(current_user_username)
                post.save()

        elif action == 'Delete' and delete_post_form.validate():
            post = Post.objects(id=post_id).first()  # Changed Review to Post
            if post:
                post.delete()

        return redirect(url_for('posts.user_detail', username=username))

    return render_template(
        "user_detail.html", 
        user_posts=user_posts, 
        user=user, 
        image=img, 
        like_post_form=like_post_form,
        delete_post_form=delete_post_form,
        joined_date=user.joined_date,
    )

@posts.route("/custom_404")
def custom_404():
    return render_template("404.html", error="404: Page not found")
