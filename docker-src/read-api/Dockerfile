# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

ADD . /read-api
WORKDIR /read-api

RUN pip3 install -r requirements.txt


CMD [ "python", "read_ado_api.py"]
