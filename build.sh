#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Current directory: $(pwd)"
echo "Listing directory contents:"
ls -la

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Debug Python/Django setup
echo "Python path:"
python -c "import sys; print(sys.path)"
echo "Django version:"
python -c "import django; print(django.__version__)"
echo "Module configuration:"
python -c "import os; print(os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set'))"

# Set correct settings module explicitly
export DJANGO_SETTINGS_MODULE=task_manager.settings

# Verify settings module can be imported
echo "Trying to import settings module..."
python -c "import task_manager.settings; print('Settings module imported successfully')"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Create test user if it doesn't exist
echo "Creating test user..."
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

echo "Build script completed successfully!" 