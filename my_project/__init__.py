from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# configure Flask using environment variables
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

from my_project import routes #has to be down here, otherwise "cannot import 'app'"
