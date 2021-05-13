from my_project.models import User

# testing the db connection by hard coding a user
# and querying him by username
def test_user_to_db(test_db):
    user = User(
        username="elias wilde", email_address="eliaswilde@web.de", password="123456"
    )
    test_db.session.add(user)
    test_db.session.commit()

    queried_user = User.query.filter_by(username="elias wilde").first()

    assert queried_user.username == "elias wilde"
    assert queried_user.email_address == "eliaswilde@web.de"
    assert queried_user.check_password_correction("123456") is True
