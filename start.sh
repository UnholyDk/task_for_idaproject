#!/bin/bash
docker-compose build && docker-compose up -d
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --run-syncdb
