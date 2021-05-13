def test_browse_posts(client, captured_templates, test_db):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/browse' route is requested (GET)

    THEN there should be the correct `status_code`, `template.name`,
        and the correct `page_title` in the context
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/browse")

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "browse.html"

    assert "page_title" in context
    assert context["page_title"] == "Browse"


def test_browse_posts_with_mocked_db(
    client, captured_templates, mocker, fake_query_posts_and_users
):
    """
    GIVEN a Flask application configured for testing (client)
        and a mocked function

    WHEN the '/browse' route is requested (GET)

    THEN there should be the fake_users username who have created a post
    aswell as the post name, short_description, description,
    max_distance in the html content
    """
    # mock the function and return our fake users and posts
    mocker.patch(
        "my_project.routes.posts.query_posts_and_users", fake_query_posts_and_users
    )

    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/browse")

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "browse.html"

    assert "page_title" in context
    assert context["page_title"] == "Browse"

    html_content = response.data.decode()

    fake_posts, fake_users = fake_query_posts_and_users()
    for post in fake_posts:
        assert post.description in html_content
        assert post.name in html_content
        assert post.short_description in html_content
        assert str(post.max_distance) in html_content

        for user in fake_users:
            if user.id == post.owner:
                assert user.username in html_content


def test_create_post_unauthenticated(client, captured_templates):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/create' route is requested (GET) without being authorized

    THEN there should be a redirect and the correct `status_code`,
     `template.name`, and the correct `page_title` in the context
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/create", follow_redirects=True)

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "login.html"

    assert "page_title" in context
    assert context["page_title"] == "Login"


def test_create_post_authenticated(client, captured_templates, login):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/create' route is requested (GET) while being authenticated

    THEN there should be the correct `status_code`, `template.name`, (/create)
        and the correct `page_title` in the context
    """

    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/create")

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "create.html"

    assert "page_title" in context
    assert context["page_title"] == "Create"


def test_my_post_unauthenticated(client, captured_templates):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/mypost' route is requested (GET)

    THEN there should be a redirect to '/login' aswell as the
    the correct `status_code`, `template.name`,
    and the correct `page_title` in the context (login)
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/mypost", follow_redirects=True)

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "login.html"

    assert "page_title" in context
    assert context["page_title"] == "Login"


def test_my_post_authenticated(client, captured_templates, login):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/mypost' route is requested (GET) as authenticated user.

    THEN there should be the correct `status_code`, `template.name` (mypost.html),
        and the correct `page_title` in the context
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/mypost")

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "mypost.html"

    assert "page_title" in context
    assert context["page_title"] == "My Post"
