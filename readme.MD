# My Foundations Project 2021


# Installation Instructions
This will be a quick overview of steps for how to run this project on your computer locally.

## Before you start...
You should have:
- Python 3.8.x installed on your computer
- Visual Studio Code installed on your computer (im not familiar with other IDE so if you use another these steps instrucctions might vary)

### Instructions

- Clone/Download the project onto your computer.

- create a venv with the requirements.txt (exclude line 47, psycopg2==2.8.6 This is only for Heroku)

- 'pip install -r requirements.txt'

- 'source env/Scripts/activate'

- 'export FLASK_APP=main.py'

Now you should be able to run the project locally!

- 'flask run'
(on some systhem these commands might be different)

## how to...

To test the project:

> pytest --doctest-modules

To Lint the project:
> flake8 --exclude venv


### A Few Notes...

Error Note: On submitting profile informations in "profil_page" (routes, line 183).
If you submit information + pictures => Internal service error (Heroku log: integer out of range)
However you can first submit the information and afterwards the profile picture.

Dont install psycopg2==2.8.6! Requirements.txt line 47. This is only for Heroku.

(SecretNote: I havent wrote any test yet.
Since everything took longer the expexted and
I have my assestment in SE_10
this week I was not having time for it but will write test for it now)




