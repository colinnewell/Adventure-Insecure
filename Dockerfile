FROM python:3
MAINTAINER Colin Newell <colin.newell@gmail.com>

RUN groupadd -r adventure && useradd -r -g adventure adventure
COPY requirements.txt /opt/adventure/
RUN pip install -r /opt/adventure/requirements.txt
COPY src /opt/adventure/
WORKDIR /opt/adventure/
#RUN chown adventure.adventure /var/
RUN mkdir -p /var/lib/adventure/db \
    mkdir -p /var/lib/adventure/upload \
    mkdir -p /var/lib/adventure/sessions \
    && chown -R adventure.adventure /var/lib/adventure
ENV APP_SETTINGS config.ProductionConfig
ENV CONNECTION_STRING sqlite:////var/lib/adventure/db/app.db
ENV SESSION_DIR /var/lib/adventure/sessions
ENV UPLOAD_DIR /var/lib/adventure/upload
USER adventure
RUN python /opt/adventure/manage.py db upgrade
CMD uwsgi --uid adventure --ini /opt/adventure/uwsgi.ini
