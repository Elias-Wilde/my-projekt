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

# importing from other files and librarys

# tell the database when the user was logged in last
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# main page
@app.route("/")
@app.route("/landing_page")
def landing_page():
    return render_template("landing_page.html", page_title="My great website")


# browse post's page
@app.route("/browse", methods=["GET", "POST"])
def browse_page():
    posts = Post.query.all()  # get all post's
    users = User.query.all()  # get all user's
    if (
        posts != []
    ):  # if empty it should return the blank page with the heading + flash message
        return render_template(
            "browse.html", page_tittle="Browse", posts=posts, users=users
        )  # render the template with posts= all post's and users= all users
    else:
        flash(f"No posts yet.", category="danger")
    return render_template(
        "browse.html", page_tittle="Browse", posts=posts, users=users
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
            owner=current_user.id,
        )
        db.session.add(post_to_create)  # add and commit to database => Post
        db.session.commit()
        flash(
            f"Listening/Post created succesfully!", category="success"
        )  # succes message and redirect to landing_page.html
        return redirect(url_for("landing_page"))
    if (
        form.errors != {}
    ):  # if validators fail => error message and returned to create.html
        for err_msg in form.errors.values():
            flash(f"Error with creating listening/post: {err_msg}", category="danger")
    return render_template("create.html", page_title="Landing Page", form=form)


# your own post's page
@app.route("/mypost", methods=["GET", "POST"])
def mypost_page():
    posts = Post.query.filter_by(
        owner=current_user.id
    ).all()  # get the post where owner ID is equal to current user ID
    if posts != []:
        return render_template("mypost.html", page_tittle="My Post", posts=posts)
    else:  # if no post's yet => error message
        flash(
            f"No post yet!",
            category="danger",
        )
        return render_template("mypost.html", page_tittle="My Post", posts=posts)


# register page
@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()  # get the register form from import at top (Forms.py)
    if form.validate_on_submit():  # validators
        user_to_create = User(  # set user_to_create to form data
            user_name=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data,
        )
        db.session.add(
            user_to_create
        )  # add and commit user_to_create to the Database, User
        db.session.commit()
        login_user(user_to_create)  # log the user_to_create in
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


# login page
@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()  # get the LoginForm from import at top (Forms.py)
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            user_name=form.username.data
        ).first()  # query the attempted login user by the username (the form input)
        # check if the user_name and the password
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)  # login success
            flash(
                f"Succesfully logged in as: {attempted_user.user_name}",
                category="success",
            )
            return redirect(url_for("landing_page"))
        else:  # login failed
            flash(
                f"Username and password did not match! Please try again",
                category="danger",
            )
    return render_template("login.html", form=form)


# logout page
@app.route("/logout")  # logout the current user and return the landing page
def logout_page():
    logout_user()
    flash(f"Succesfully logged out!", category="info")
    return redirect(url_for("landing_page"))


# save profile pictures as random hex
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = 125, 125  # store picture as 125x125
    # pillow library used to make the picture a even square
    # this is important because the picture is displayed "round" and would else stretch
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


# profile page
@app.route("/profile", methods=["GET", "POST"])
def profile_page():
    form = ProfileForm()  # set form to ProfileForm imported at top (forms.py)
    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file
    )  # get the current user image file
    # update the DB, User with the data from the ProfileForm
    if request.method == "POST":
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.full_name = form.full_name.data
            current_user.ort = form.ort.data
            current_user.postleitzahl = form.postleitzahl.data
            current_user.address = form.address.data
            current_user.phone_number = form.phone_number.data
            db.session.commit()
            flash(
                f"Profile succesfully updated, {current_user.user_name}",
                category="success",
            )
            return render_template(
                "profile.html", form=form
            )  # return the profile page with updated infos
        if (
            form.errors != {}
        ):  # checks for validations erros. if form.errors is not empty the error is raised
            for err_msg in form.errors.values():
                flash(
                    f"Error with updating your profile, : {err_msg}", category="danger"
                )
    else:  # prefill the form if already filled in earlier
        filled_form = ProfileForm(obj=current_user)
        return render_template(
            "profile.html",
            page_title="Profile",
            form=filled_form,
            image_file=image_file,
        )


# getting started / read more page
@app.route("/get_started")
def get_started_page():
    return render_template("get_started.html", page_title="Get Started")