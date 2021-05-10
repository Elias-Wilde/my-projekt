# try:
#     from my_project import app, db
#     from my_project.models import User
#     import pytest
# except Exception as a:
#     print("something is missing."(a))


# def test_index():
#     # create a version of our website that we can use for testing
#     with app.test_client() as test_client:
#         # mimic a browser: 'GET /', as if you visit the site
#         response = test_client.get('/')

#         # check that the HTTP response is a success
#         assert response.status_code == 200

#         # Store the contents of the html response in a local variable.
#         # This should be a string with the same content as the file index.html
#         html_content = response.data.decode()

#         assert '<html lang="en">' in html_content

# # @pytest.fixture
# # def client():
# #     app = app()
# #     app.config["TESTING"] = True
# #     app.testing = True
# #     # test db
# #     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

# #     client = app.test_client()
# #     with app.app_context():
# #         db.create_all()
# #         user1 = User(id=1, user_name="elias", email_address="elias@email.com")
# #         db.session.add(user1)
# #         db.session.commit()
# #     yield client

# # def test_user(client) -> None:
# #     rv = client.get("/user/1")
# #     assert rv.json == {"id":1,"user_name": "elias", "email_address": "elias@email.com"}

# # def test_new_user():
# #     user = User('someuser','someuser@web.de','123456')
# #     assert user.email_address == 'someuser@web.de'
# #     assert user.user_name == 'someuser'
# #     assert user.password_hash != '123456'

