#!/bin/sh
python update_projects.py
crond
exec gunicorn -b 0.0.0.0:5000 main:app
