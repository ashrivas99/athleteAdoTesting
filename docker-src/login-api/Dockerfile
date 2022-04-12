# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

ADD . /login-api
WORKDIR /login-api

RUN pip3 install -r requirements.txt

CMD [ "python", "login_api.py"]
