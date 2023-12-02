import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required, login_user, logout_user

from .. import movie_client
from ..forms import MovieReviewForm, SearchForm
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..forms import LikePostForm
from ..models import User, Review
from ..utils import current_time
from .. import bcrypt

movies = Blueprint("movies", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """

@movies.context_processor
def context_processor():
    return {'search_form': SearchForm()}

@movies.route("/", methods=["GET", "POST"])
def index():
    search_form = SearchForm()
    post_form = MovieReviewForm()
    like_post_form = LikePostForm()

    if search_form.validate_on_submit():
        return redirect(url_for("movies.query_results", query=search_form.search_query.data))

    if post_form.validate_on_submit():
        user = current_user._get_current_object()
        img = get_b64_img(user.username)

        review = Review(
            commenter=current_user._get_current_object(),
            content=post_form.text.data,
            date=current_time(),
            imdb_id="Feed",
            image=img,
            movie_title="Timeline",
            likes=[],
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id="Feed")

    return render_template(
        "index.html", 
        search_form=search_form,
        post_form=post_form,
        user_posts=reviews,
        like_post_form=like_post_form,
    )

@movies.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = movie_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@movies.route("/movies/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    form = MovieReviewForm()
    
    if form.validate_on_submit():
        user = current_user._get_current_object()
        img = get_b64_img(user.username)

        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            image=img,
            movie_title=result.title,
            likes=[],
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html", 
        form=form, 
        movie=result, 
        reviews=reviews
    )

#Done ?
@movies.route("/user/<username>", methods=['GET', 'POST'])
def user_detail(username):
    #uncomment to get review image
    #user = find first match in db
    #img = get_b64_img(user.username) use their username for helper function
    user = User.objects(username=username).first()

    if user is None:
        error = "User not found"
        return render_template("user_detail.html", error=error, image=None)
    
    error = None

    user_posts = Review.objects(commenter=user.id)
    img = get_b64_img(user.username)
    
    like_post_form = LikePostForm()
    
    if request.method == 'POST':
        if like_post_form.validate_on_submit():
            review_id = like_post_form.review_id.data
            review = Review.objects(id=review_id).first()
            if review:
                if current_user.id in review.likes:
                    review.likes.remove(current_user.id)
                else:
                    review.likes.append(current_user.id)
                review.save()
            return redirect(url_for('user_detail', username=current_user.username))

    return render_template(
        "user_detail.html", 
        user_posts=user_posts, 
        user=user, 
        image=img, 
        error=error,
        like_post_form=like_post_form,
    )

@movies.route("/custom_404")
def custom_404():
    #flash("404: Page not found", "error")
    return render_template("404.html", error="404: Page not found")