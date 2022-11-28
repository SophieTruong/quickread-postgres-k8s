# pull official base image
FROM python:3.8.10-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install flake8==6.0.0
RUN flake8 --ignore=E501,E226,E302,E41 --max-line-length=160 .

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]