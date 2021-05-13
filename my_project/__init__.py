from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from sqlalchemy_utils import create_database, database_exists

app = Flask(__name__)
# configure Flask using environment variables
# app.config.from_pyfile("config.py")

# not using the config file right now because I had problems with heroku getting the Database URL
if os.environ.get("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace(
        "://", "ql://", 1
    )
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_project.db"

app.config["SECRET_KEY"] = "SECRET_KEY"

# database instance
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


# has to be down here, otherwise "cannot import 'app', circular error"
from my_project import routes


if app.config['ENV'] == 'production':
    # create db tables
    from my_project.models import User, Post
    db.create_all()
    db.session.commit()
