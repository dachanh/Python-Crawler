#!/bin/bash
export FLASK_APP=main.py
flask db init
flask db migrate
flask db upgrade
gunicorn main:app --bind 0.0.0.0:8181 --workers 5