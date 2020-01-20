FROM python:3.7.6-buster

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev python3-setuptools --no-install-recommends

ENV INSTALL_PATH /api
RUN mkdir $INSTALL_PATH
WORKDIR $INSTALL_PATH

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python app.py