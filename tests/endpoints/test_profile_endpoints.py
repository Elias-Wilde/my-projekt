def test_profile_unauthenticated(client, captured_templates):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/profile' route is requested (GET) without being
        logged in

    THEN there should be the correct `status_code`, `template.name`,
        and the correct `page_title` in the context and redirected to login
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/profile", follow_redirects=True)

    # check that the HTTP response is a redirect (since user is not logged in)
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "login.html"

    assert "page_title" in context
    assert context["page_title"] == "Login"

