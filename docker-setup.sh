#!/bin/bash

#update code for images
cp backend/services_and_apis/login_api.py docker-src/login-api/
cp backend/services_and_apis/read_ado_api.py docker-src/read-api/
cp backend/services_and_apis/write_athlete_api.py docker-src/write-api/

# install venv and requirements
if [ ! -f venv/bin/activate ]
then
    /usr/bin/python3.9 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi


for file in ./docker-src/*/; do 
    cp ./requirements.txt ./"$file"
    cp  backend/services_and_apis/database.py ./"$file"
done

