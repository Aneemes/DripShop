#!/bin/bash

# Run database migrations or initialization tasks
echo "Running database migrations..."
python manage.py makemigrations --settings=dripshop.settings.dev
python manage.py migrate --settings=dripshop.settings.dev

# Start the development server
echo "Starting Django application..."
python manage.py runserver 0.0.0.0:8000 --settings=dripshop.settings.dev
