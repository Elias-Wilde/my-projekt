# file to configure flask, loaded into our flask application
# using the line: app.config.from_pyfile("config.py") in website.py
from os import environ

# These variables be available to your application to use.
# Things that may be different on different computers, like a path to a file,
# should go in here. This is all available in GitHub, so be careful.

# For example, you can add the port you wish to run on as a variable.
# This can then be used when running the code.
MY_PORT = "5000"

#DATABASE_PASSWORD = environ.get("DB_PASSWORD")

# if environ.get('DATABASE_URL'):
#   # Set the database URL from the environment variable if it is set.
#   # The .replace() is a workaround because of a mismatch between Heroku's default set up and SQLAlchemy
#   SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL').replace("://", "ql://", 1)
# else:
#   # Use SQLite as a fallback and locally
#   SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI") #"sqlite:///my_project.db"

SQLALCHEMY_TRACK_MODIFICATIONS = False  # TODO google das noch mal

SECRET_KEY = environ.get("SECRET_KEY")
