import os
import secrets
from PIL import Image
from flask_login.utils import login_required
from my_project import app
from flask import render_template, url_for, flash, request
from my_project.forms import ProfileForm
from my_project import db
from flask_login import current_user


def crop_picture_to_square(picture):
    """
    Pillow library used to make the picture an even square.

    This is important because the picture is displayed "round" and would else stretch.
    """
    i = Image.open(picture)
    width, height = i.size
    width_offset = 0
    height_offset = 0
    if width > height:
        width_offset = (width - height) / 2
    else:
        height_offset = (height - width) / 2
    return i.crop(
        (width_offset, height_offset, width - width_offset, height - height_offset)
    )


# save profile pictures as random hex
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = 125, 125  # store picture as 125x125

    i = crop_picture_to_square(form_picture)

    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# profile page
@app.route("/profile", methods=["GET", "POST"])
@login_required
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
                f"Profile succesfully updated, {current_user.username}",
                category="success",
            )
            return render_template(
                "profile.html", page_title="Profile", form=form
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