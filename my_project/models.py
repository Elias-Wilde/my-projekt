from my_project import db, login_manager
from my_project import bcrypt
from flask_login import (
    UserMixin,
)  # press f12 on 'userMixin, it contains methods/properties we need for user login
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(length=25), nullable=False, unique=True)
    email_address = db.Column(db.String(length=40), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    post = db.relationship(
        "Post", backref="owned_user", lazy=True
    )  # relation to post's

    full_name = db.Column(db.String(length=50), nullable=True, unique=False)
    ort = db.Column(db.String(length=30), unique=False)
    postleitzahl = db.Column(db.Integer, unique=False)
    address = db.Column(db.String(length=100), unique=False)
    friends_list = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP())
    phone_number = db.Column(db.Integer)
    image_file = db.Column(db.String(), nullable=False, default="default.png")
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

#Post model
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=60), nullable=False, unique=False)
    short_description = db.Column(db.String(length=80), nullable=False, unique=False)
    description = db.Column(db.String(length=500), nullable=False, unique=False)
    max_distance = db.Column(db.Integer(), nullable=False, unique=False, default=5)
    service_start_date = db.Column(db.DateTime, default=datetime.utcnow)
    service_end_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_public = db.Column(db.String())
    created_at = db.Column(db.TIMESTAMP())
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"))
