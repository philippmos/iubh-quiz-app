#!/bin/bash

cd ../web-bundle
npm run dev:build


cd ../web-app
source antenv/bin/activate

gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
# python app.py runserver