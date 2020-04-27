#!/bin/sh
source venv/bin/activate
# exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app

# https://stackoverflow.com/questions/35837786/how-to-run-flask-with-gunicorn-in-multithreaded-mode
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:APP -w 4 --threads 6
