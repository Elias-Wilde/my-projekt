def test_register_get(client, captured_templates):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/' route is requested (GET)

    THEN there should be the correct `status_code`, `template.name`,
        and the correct `page_title` in the context
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/register")

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "register.html"

    assert "page_title" in context
    assert context["page_title"] == "Register"


def test_valid_register_post(client, captured_templates, test_db):
    """
    GIVEN a Flask application configured for testing (client), the test db

    WHEN a user wants to register and posts valid data to '/register' (POST)

    THEN the user should be registered to the db, logged in, and
        redirected to the landing page.
    """
    # mimic a browser: 'POST /register', as if you visit the site
    response = client.post(
        "/register",
        data=dict(
            username="28kadsen",
            email_address="28kadsen@gmail.com",
            password1="123456",
            password2="123456",
        ),
        follow_redirects=True,
    )

    # check that the HTTP response fail
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "landing_page.html"

    assert "page_title" in context
    assert context["page_title"] == "Help & Help"

    html_content = response.data.decode()
    assert '<a class="nav-link" href="#">Welcome, 28kadsen</a>' in html_content


def test_invalid_register_post(client, captured_templates, test_db):
    """
    GIVEN a Flask application configured for testing (client) and the test db

    WHEN a user wants to register and posts invalid data to '/register' (POST)

    THEN the user should NOT be registered to the db, html contain error messages.
    """
    # mimic a browser: 'POST /register', as if you visit the site
    response = client.post(
        "/register",
        data=dict(
            username="gottheit",
            email_address="28kadsengmail.com",
            password1="44444",
            password2="55555",
        ),
        follow_redirects=True,
    )

    # check that the HTTP response is a success
    assert response.status_code == 400

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "register.html"

    assert "page_title" in context
    assert context["page_title"] == "Register"

    html_content = response.data.decode()

    assert "Invalid email address." in html_content
    assert "Field must be equal to password1." in html_content


def test_login_get(client, captured_templates):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/login' route is requested (GET)

    THEN there should be the correct `status_code`, `template.name`,
        and the correct `page_title` in the context
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/login")

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "login.html"

    assert "page_title" in context
    assert context["page_title"] == "Login"


def test_login_post(client, captured_templates, fake_user):
    """
    GIVEN a Flask application configured for testing (client) and the fake_user

    WHEN the fake_user data is posted

    THEN then the fake_user should be logged in and redirected to the landing page
    """
    # mimic a browser: 'POST /', as if you visit the site
    response = client.post(
        "/login",
        data=dict(username=fake_user.username, password="123456"),
        follow_redirects=True,
    )

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "landing_page.html"

    assert "page_title" in context
    assert context["page_title"] == "Help & Help"


def test_logout(client, captured_templates):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/logout' route is requested (GET)

    THEN the user should be logged out and
    there should be the correct `status_code`, `template.name`,
    and the correct `page_title` in the context
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/logout", follow_redirects=True)

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "login.html"

    assert "page_title" in context
    assert context["page_title"] == "Login"
