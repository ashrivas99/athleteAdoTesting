# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
ADD . /write_api
WORKDIR /write_api

RUN pip3 install -r requirements.txt

CMD [ "python", "write_athlete_api.py"]
