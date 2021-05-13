from my_project import app
from flask import render_template, redirect, url_for, flash
from my_project.forms import PostForm
from my_project.models import User, Post
from my_project import db
from flask_login import login_required, current_user


def query_posts_and_users():
    posts = Post.query.all()  # get all post's
    users = User.query.all()  # get all user's
    return (posts, users)


# browse post's page
@app.route("/browse")
def browse_page():
    posts, users = query_posts_and_users()
    if (
        posts != []
    ):  # if empty it should return the blank page with the heading + flash message
        return render_template(
            "browse.html", page_title="Browse", posts=posts, users=users
        )  # render the template with posts= all post's and users= all users
    else:
        flash("No posts yet.", category="danger")
    return render_template(
        "browse.html", page_title="Browse", posts=posts, users=users
    )


# create a post page
@app.route("/create", methods=["GET", "POST"])
@login_required  # only accescible if logged in
def create_page():
    form = PostForm()  # get the PostForm from import at top (Forms.py)
    if form.validate_on_submit():  # chech validators
        post_to_create = Post(
            name=form.name.data,
            short_description=form.short_description.data,
            description=form.description.data,
            max_distance=form.max_distance.data,
            service_start_date=form.service_start_date.data,
            service_end_date=form.service_end_date.data,
            is_public=form.is_public.data,
            owner=current_user.id
        )
        db.session.add(post_to_create)  # add and commit to database => Post
        db.session.commit()
        flash(
            "Listening/Post created succesfully!", category="success"
        )  # succes message and redirect to landing_page.html
        return redirect(url_for("landing_page"))
    if (
        form.errors != {}
    ):  # if validators fail => error message and returned to create.html
        for err_msg in form.errors.values():
            flash(f"Error with creating listening/post: {err_msg}", category="danger")
    return render_template("create.html", page_title="Create", form=form)


# your own post's page
@app.route("/mypost", methods=["GET", "POST"])
@login_required
def mypost_page():
    posts = Post.query.filter_by(
        owner=current_user.id
    ).all()  # get the post where owner ID is equal to current user ID
    if posts != []:
        return render_template("mypost.html", page_title="My Post", posts=posts)
    else:  # if no post's yet => error message
        flash("No post yet!", category="danger")
        return render_template("mypost.html", page_title="My Post", posts=posts)
