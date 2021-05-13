from my_project import app
from flask import render_template
from my_project import db
from flask_login import current_user
from datetime import datetime

# import other routes
from . import auth, posts, profile


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
    return render_template("landing_page.html", page_title="Help & Help")


# getting started / read more page
@app.route("/get_started")
def get_started_page():
    return render_template("get_started.html", page_title="Get Started")
