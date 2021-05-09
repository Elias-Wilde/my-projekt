import os
import secrets
from PIL import Image
from my_project import app
from flask import render_template, redirect, url_for, flash, request
from my_project.forms import RegisterForm, LoginForm, ProfileForm, PostForm
from my_project.models import User, Post
from my_project import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/landing_page")
def landing_page():
    return render_template("landing_page.html", page_title="My great website")


@app.route("/browse", methods=["GET", "POST"])  #error handling? if empty it should return the blank page with the heading + flash message
def browse_page():
    posts = Post.query.all()
    users = User.query.all()
    if posts != []:
        return render_template("browse.html", page_tittle="Browse", posts=posts, users=users)
    else:
        flash(f"No posts yet.", category="danger")
    return render_template("browse.html", page_tittle="Browse", posts=posts, users=users)



# @app.route("/post_details", methods=["GET", "POST"])
# def post_details_page():
#     return render_template("post_details.html", page_tittle="Post details")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create_page():
    form = PostForm()
    if form.validate_on_submit():
        post_to_create = Post(
            name=form.name.data,
            short_description=form.short_description.data,
            description=form.description.data,
            max_distance=form.max_distance.data,
            service_start_date=form.service_start_date.data,
            service_end_date=form.service_end_date.data,
            is_public=form.is_public.data,
            owner=current_user.id,
        )
        db.session.add(post_to_create)
        db.session.commit()
        flash(f"Listening/Post created succesfully!", category="success")
        return redirect(url_for("landing_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error with creating listening/post: {err_msg}", category="danger")
    return render_template("create.html", page_title="Landing Page", form=form)


@app.route("/mypost", methods=["GET", "POST"])
def mypost_page():
    posts = Post.query.filter_by(owner=current_user.id).all()
    if posts != []:
        return render_template("mypost.html", page_tittle="My Post", posts=posts)
    else:
        flash(
            f"No post yet!",
            category="danger",
        )
        return render_template("mypost.html", page_tittle="My Post", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            user_name=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f"Account created succesfully and loged in as {user_to_create.user_name}",
            category="success",
        )
        return redirect(url_for("landing_page"))
    if (
        form.errors != {}
    ):  # checks for validations erros. if {} is empty the error is raised
        for err_msg in form.errors.values():
            flash(f"Error with creating your account: {err_msg}", category="danger")
    return render_template("register.html", page_title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(user_name=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Succesfully logged in as: {attempted_user.user_name}",
                category="success",
            )
            return redirect(url_for("landing_page"))
        else:
            flash(
                f"Username and password did not match! Please try again",
                category="danger",
            )
    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash(f"Succesfully logged out!", category="info")
    return redirect(url_for("landing_page"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = 125, 125
    i = Image.open(form_picture)
    width, height = i.size
    width_offset = 0
    height_offset = 0
    if width > height:
        width_offset = (width - height) / 2
    else:
        height_offset = (height - width) / 2
    i_cropped = i.crop(
        (width_offset, height_offset, width - width_offset, height - height_offset)
    )
    i_cropped.thumbnail(output_size)
    i_cropped.save(picture_path)

    return picture_fn


@app.route("/profile", methods=["GET", "POST"])
def profile_page():
    form = ProfileForm()
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)

    if request.method == "POST":
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.full_name = form.full_name.data
            current_user.ort = form.ort.data
            current_user.postleitzahl = form.postleitzahl.data
            current_user.address = form.address.data
            db.session.commit()
            flash(
                f"Profile succesfully updated, {current_user.user_name}",
                category="success",
            )
            return render_template("profile.html", form=form)
        if (
            form.errors != {}
        ):  # checks for validations erros. if form.errors is not empty the error is raised
            for err_msg in form.errors.values():
                flash(
                    f"Error with updating your profile, : {err_msg}", category="danger"
                )
    else:
        filled_form = ProfileForm(
            obj=current_user
        )  # prefill the form if already filled in earlier
        return render_template(
            "profile.html",
            page_title="Profile",
            form=filled_form,
            image_file=image_file,
        )


@app.route("/get_started")
def get_started_page():
    return render_template("get_started.html", page_title="Get Started")