from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# configure Flask using environment variables
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from my_project import (
    routes,
)  # has to be down here, otherwise "cannot import 'app', circular error"
