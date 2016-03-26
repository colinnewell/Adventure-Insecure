FROM python:3
MAINTAINER Colin Newell <colin.newell@gmail.com>

RUN groupadd -r adventure && useradd -r -g adventure adventure
COPY requirements.txt /opt/adventure/
RUN pip install -r /opt/adventure/requirements.txt
COPY src /opt/adventure/
ENV DATABASE_URL=fixme
ENV APP_SETTINGS=config.ProductionConfig
WORKDIR /opt/adventure/
RUN python /opt/adventure/manage.py db upgrade
CMD uwsgi --uid adventure --ini /opt/adventure/uwsgi.ini
