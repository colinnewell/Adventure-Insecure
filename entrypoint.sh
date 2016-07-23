#!/bin/sh
# first we ensure the db is up to date with the code.
python /opt/adventure/manage.py db upgrade
uwsgi --uid adventure --ini /opt/adventure/uwsgi.ini
