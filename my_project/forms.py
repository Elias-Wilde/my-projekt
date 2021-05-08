from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    DateField,
    RadioField,
)
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed
from my_project.models import User


class RegisterForm(FlaskForm):
    def validate_username(
        self, username_to_check
    ):  # has to be name 'validate_username' since we named it 'username' down below
        user = User.query.filter_by(user_name=username_to_check.data).first()
        if user:
            raise ValidationError("Username already taken!")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(
            email_address=email_address_to_check.data
        ).first()
        if email_address:
            raise ValidationError("Email address already registert!")

    username = StringField(
        label="User Name:", validators=[Length(min=3, max=15), DataRequired()]
    )
    email_address = StringField(
        label="Email Address:", validators=[Email(), DataRequired()]
    )
    password1 = PasswordField(
        label="Password:", validators=[Length(min=6, max=25), DataRequired()]
    )
    password2 = PasswordField(
        label="Confirm Password:", validators=[EqualTo("password1"), DataRequired()]
    )
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label="User Name:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Login")


class ProfileForm(FlaskForm):

    full_name = StringField(label="Full Name:", validators=[Length(min=5, max=35)])
    ort = StringField(label="Ort:", validators=[Length(min=3, max=30)])
    postleitzahl = IntegerField(label="zip code:")
    address = StringField(label="Address:", validators=[Length(min=5, max=40)])
    picture = FileField(
        label="Profile Picture:", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField(label="Update Profile")

    # def __init__(self, full_name, ort, postleitzahl, address):
    #     self.full_name = full_name
    #     self.ort = ort
    #     self.postleitzahl = postleitzahl
    #     self.address = address


class PostForm(FlaskForm):
    name = StringField(
        label="Listening display Name:", validators=[Length(min=12, max=60)]
    )
    short_description = StringField(
        label="Add a short description:", validators=[Length(min=20, max=80)]
    )
    description = StringField(
        label="Detailed description:", validators=[Length(min=80, max=500)]
    )
    service_start_date = DateField()
    service_end_date = DateField()
    max_distance = IntegerField(label="Enter max distance:")
    is_public = RadioField(
        label="Public listening:", choices=[("yes", "public"), ("no", "private")]
    )
    submit = SubmitField(label="Create Listening")
