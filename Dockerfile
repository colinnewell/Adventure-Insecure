FROM python:3
MAINTAINER Colin Newell <colin.newell@gmail.com>

RUN groupadd -r adventure && useradd -r -g adventure adventure
COPY requirements.txt /opt/adventure/
RUN pip install -r /opt/adventure/requirements.txt
COPY src /opt/adventure/
WORKDIR /opt/adventure/
RUN mkdir -p /var/lib/adventure/db \
    && mkdir -p /var/lib/adventure/upload \
    && mkdir -p /var/lib/adventure/sessions \
    && mkdir -p /var/lib/adventure/menus \
    && chown -R adventure.adventure /var/lib/adventure
ENV APP_SETTINGS config.ProductionConfig
# NOTE: this sqlite db is setup so that the box can potentially
# run standalone.
# This can be overridden at run time.
ENV CONNECTION_STRING sqlite:////var/lib/adventure/db/app.db
ENV SESSION_DIR /var/lib/adventure/sessions
ENV UPLOAD_DIR /var/lib/adventure/upload
ENV MENUS_DIR /var/lib/adventure/menus
ENV LDAP_SERVER ldap
COPY entrypoint.sh /entrypoint.sh
USER adventure
RUN python /opt/adventure/manage.py db upgrade
CMD /entrypoint.sh
