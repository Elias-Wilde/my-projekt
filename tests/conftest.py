import pytest
from flask import template_rendered
from my_project import app, db
from my_project.models import User, Post
from sqlalchemy_utils import create_database, database_exists

TESTDB = "test_db.db"
TEST_DATABASE_URI = "sqlite:///" + TESTDB

# creates all tables and drops them at the end
@pytest.fixture
def test_db(test_app):
    """
    Does a database rollback on a function based scope and
    closes the session after execution is completed.

    NOTE: when running pytest in parallel (multiple functions at the same time) this way
    of doing a rolleback it may happend that one test is doing a rolleback while the other is
    still using the database.
    """
    with test_app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.close()
        db.drop_all()


# create the db if not exists alrdy
@pytest.fixture(scope="session")
def setup_db():
    if not database_exists(TEST_DATABASE_URI):
        create_database(TEST_DATABASE_URI)


# test app configurations, db uri and crsf token enabled
@pytest.fixture(scope="session")
def test_app():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URI
    app.config["WTF_CSRF_ENABLED"] = False

    yield app


# flask application client for testing
@pytest.fixture
def client(test_app):

    # Create test client using the Flask application configured for testing
    with test_app.test_client() as test_client:
        # Establish an application context
        with test_app.app_context():
            yield test_client


@pytest.fixture
def captured_templates(test_app):
    """
    captures the templates returned by flask while a test

    NOTE: When making multiple requests to the `test_client` during
    a test it may happen that multiple templates are returned.
    """
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, test_app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, test_app)


# creates a fake user and commits it to the test database
@pytest.fixture
def fake_user(test_db):
    user = User(
        username="elias wilde", email_address="eliaswilde@web.de", password="123456"
    )
    test_db.session.add(user)
    test_db.session.commit()
    yield user


# disables the `@login_required` decorator by `flask_login` library
@pytest.fixture
def disable_login_required(test_app):
    test_app.config["LOGIN_DISABLED"] = True
    yield
    test_app.config["LOGIN_DISABLED"] = False


# logs the fake user in before the test and logs out after the test
@pytest.fixture
def login(client, fake_user):
    client.post("/login", data=dict(username="elias wilde", password="123456"))
    yield
    client.get("/logout")

# create version of the user and post query function to mock the the functions
@pytest.fixture
def fake_query_posts_and_users():
    fake_users = [
        User(
            id=1,
            username="gottheit",
            email_address="derallerechte@web.de",
            password="123456",
        ),
        User(
            id=2,
            username="max",
            email_address="maxmustermann@web.de",
            password="123456",
        ),
    ]
    fake_posts = [
        Post(
            id=1,
            name="erster post",
            short_description="zwanzig zeichen oh no",
            description="hanz vile zeichen müssen hier rein och komm shcon i hope its enough now",
            max_distance=8,
            owner=1,
        ),
        Post(
            id=2,
            name="Some Name",
            short_description="Some short description.",
            description="Some description that is a bit longer than the short description",
            max_distance=10,
            owner=2,
        ),
    ]
    # return the queried fake user and post
    def fake_query_func():
        return (fake_posts, fake_users)

    return fake_query_func
