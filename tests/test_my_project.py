from my_project import app


# def test_index():
#     # create a version of our website that we can use for testing
#     with app.test_client() as test_client:
#         # mimic a browser: 'GET /', as if you visit the site
#         response = test_client.get('/')

#         # check that the HTTP response is a success
#         assert response.status_code == 200


#         # IS THIS FAILING CAUSE OF BOOTSTRAP??????
#         # Store the contents of the html response in a local variable.
#         # This should be a string with the same content as the file index.html
#         html_content = response.data.decode()

#         assert '<html lang="en">' in html_content
