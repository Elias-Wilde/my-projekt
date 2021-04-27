from my_project import app
from flask import render_template, redirect, url_for, flash
from my_project.forms import RegisterForm
from my_project.models import User
from my_project import db



@app.route("/")
@app.route("/landing_page")
def landing_page():
    return render_template("landing_page.html", page_title="My great website")


@app.route("/browse")
def browse_page():
    users = User.query.all()
    return render_template("browse.html", page_title="Browse", users=users)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            user_name=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("browse_page"))
    if form.errors != {}: #checks for validations erros. if {} is empty the error is raised
        for err_msg in form.errors.values():
            flash(f'Error with creating your account: {err_msg}', category='danger')
    return render_template("register.html", page_title="Register", form=form)
