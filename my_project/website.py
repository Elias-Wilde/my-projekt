from flask import Flask
from flask import render_template

app = Flask(__name__)

# configure Flask using environment variables
app.config.from_pyfile("config.py")


@app.route('/')
def landing_page():
    return render_template('landing_page.html', page_title="My great website")


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
