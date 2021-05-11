# My Foundations Project 2021 - Short description

The Idea of the website is to enable communitys to connect in order to help and share among the community members.
What ever you need help with (example: shopping assistance) you will most likely find a voluntere to help you out.
On the other hand you can create posts and offer whatever you got to offer for your community, help / goods / guidance / company.
The idea is to build neighborhood communitys.


# Installation Instructions
This will be a quick overview of steps for how to run this project on your computer locally.

## Before you start...
You should have:
- Python 3.8.x installed on your computer
- Visual Studio Code installed on your computer (im not familiar with other IDE so if you use another these steps instrucctions might vary)

### Instructions

- Clone/Download the project onto your computer.

- create a venv with the requirements.txt (exclude line 47, psycopg2==2.8.6 This is only for Heroku)

- `pip install -r requirements.txt`

- `source env/Scripts/activate`

- `export FLASK_APP=main.py`

- Create a .env file in the root directory of your project. Define the "SQLALCHEMY_DATABASE_URI" and "SECRET_KEY" and create the db with:
- `python`
- `from my_project import db`
- `db.create_all()`
- `exit`

Now you should be able to run the project locally!

- `flask run`
(on some systhem these commands might be different)

## how to...

To test the project:

> pytest --doctest-modules

To Lint the project:
> flake8 --exclude venv

### A Few Notes...

Dont install psycopg2==2.8.6! Requirements.txt line 47. This is only for Heroku.

(SecretNote: I havent wrote any test yet.
Since everything took longer the expexted and
I have my assestment in SE_10
this week I was not having time for it but will write test for it now)




