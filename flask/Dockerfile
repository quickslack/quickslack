FROM continuumio/anaconda:latest

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /flask
RUN mkdir $INSTALL_PATH
WORKDIR $INSTALL_PATH

ENV PYTHONUNBUFFERED 1

COPY environment.yml environment.yml
RUN conda update -n base -c defaults conda
RUN conda env create -f environment.yml
RUN /bin/bash -c ". activate quickslack"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN pip install --editable .

CMD gunicorn -c "python:config.gunicorn" "quickslack.app:create_app()"