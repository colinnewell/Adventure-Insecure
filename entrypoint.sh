#!/bin/sh
# first we ensure the db is up to date with the code.
echo "Wait until database is ready..."
until nc -z db 5432
do
    sleep 1
done
python /opt/adventure/manage.py db upgrade
uwsgi --uid adventure --ini /opt/adventure/uwsgi.ini
