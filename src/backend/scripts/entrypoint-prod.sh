#!/bin/bash
python3 src/backend/manage.py makemigrations --no-input
python3 src/backend/manage.py migrate --no-input
