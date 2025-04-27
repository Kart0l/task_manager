#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

# Create test user if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='user').exists():
    User.objects.create_user(
        username='user',
        password='user12345.',
        email='user@example.com',
        first_name='Test',
        last_name='User'
    )
    print('Test user created')
else:
    print('Test user already exists')
" 