FROM python:3
MAINTAINER Colin Newell <colin.newell@gmail.com>

RUN apt-get update && apt-get install -y netcat
RUN groupadd -r adventure && useradd -r -d /home/adventure -g adventure adventure
COPY requirements.txt /opt/adventure/
RUN pip install -r /opt/adventure/requirements.txt
# NOTE: using fork by moreati
# https://github.com/moreati/python-zxcvbn
# for Python 3 support.
COPY zxcvbn-1.0.tar.gz /root/zxcvbn-1.0.tar.gz
RUN pip install /root/zxcvbn-1.0.tar.gz
COPY src /opt/adventure/
WORKDIR /opt/adventure/
RUN mkdir -p /var/lib/adventure/db \
    && mkdir -p /var/lib/adventure/upload \
    && mkdir -p /home/adventure \
    && mkdir -p /var/lib/adventure/sessions \
    && mkdir -p /var/lib/adventure/menus \
    && chown -R adventure.adventure /var/lib/adventure /home/adventure
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
