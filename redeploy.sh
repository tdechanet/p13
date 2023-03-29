#!/bin/bash

source env/bin/activate
pip install -r requirements.txt
python workoutshare/manage.py migrate
python workoutshare/manage.py collectstatic --noinput
deactivate
sudo systemctl restart gunicorn