def test_landing_page(client, captured_templates):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/' route is requested (GET)

    THEN there should be the correct `status_code`, `template.name`,
        and the correct `page_title` in the context
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/")

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "landing_page.html"

    assert "page_title" in context
    assert context["page_title"] == "Help & Help"


def test_get_started(client, captured_templates):
    """
    GIVEN a Flask application configured for testing (client)

    WHEN the '/get_started' route is requested (GET)

    THEN there should be the correct `status_code`, `template.name`,
        and the correct `page_title` in the context
    """
    # mimic a browser: 'GET /', as if you visit the site
    response = client.get("/get_started")

    # check that the HTTP response is a success
    assert response.status_code == 200

    # check that the rendered template is the correct one
    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "get_started.html"

    assert "page_title" in context
    assert context["page_title"] == "Get Started"
