#!/bin/bash

gunicorn -b 0.0.0.0:5000 -w 1 --graceful-timeout 30 -t 60 'app.app:app'
