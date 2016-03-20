FROM python:3
MAINTAINER Colin Newell <colin.newell@gmail.com>

COPY requirements.txt /opt/adventure/
RUN pip install -r /opt/adventure/requirements.txt
COPY src /opt/adventure/
ENV DATABASE_URL=fixme
ENV APP_SETTINGS=config.ProductionConfig
CMD uwsgi --ini /opt/adventure/uwsgi.ini
