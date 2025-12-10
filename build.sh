#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python modules
pip install -r requirements.txt

# Convert static files (CSS/JS) so they work online
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate