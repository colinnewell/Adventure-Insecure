# An insecure application.

This has been archived.  Sadly the python dependencies weren't properly pinned so while the app
worked in 2016 when the talk was given it stopped working some time after and an attempt to
upgrade the deps and the code to make them work never got finished.

Don't host this publicly unless you want to provide a remote shell to hackers.

To run this properly with a Postgres database use the docker compose setup
in the docker directory.  That has additional infrastructure necessary, and
deep within the compose directory is a docker-compose file.

Some exploits may not work very well with the SQLite database.

This was developed to accompany my talk at PyConUK 2016 - An adventure in exploitation with Python

* Synopsis - http://2016.pyconuk.org/talks/an-adventure-in-exploitation-with-python/
* Slides - https://docs.google.com/presentation/d/1edFsGyEihKJZwaJAJBaJ9yDPWpOVfGZmaA7LkF3VinA/pub?start=false&loop=false&delayms=3000.
* Video - https://www.youtube.com/watch?v=Es9LjkrZT1Q

## Development

Work from the src directory,

### Setup

    apt-get install python3-dev python3-virtualenv
    virtualenv --python `which python3` env
    source env/bin/activate
    pip install -r requirements.txt

### General dev.

    APP_SETTINGS=config.DevelopmentConfig python run.py

#### Tests

    APP_SETTINGS=config.DevelopmentConfig python -m unittest

### DB Management

#### DB setup

To create or update the database to the latest version run the upgrade command.

    APP_SETTINGS=config.DevelopmentConfig python manage.py db upgrade

#### DB changes

To create a migration file for database changes run the migrate command.

    APP_SETTINGS=config.DevelopmentConfig python manage.py db migrate
