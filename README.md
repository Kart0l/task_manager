# Task Manager

A comprehensive task management application built with Django that allows users to create, assign, and track tasks with different priorities and statuses.

## Features

- **User Authentication**
  - Register/Login via email or Google OAuth
  - Role-based permissions (User, Developer, Project Manager)
  - User profiles with statistics

- **Task Management**
  - Create and assign tasks with deadlines
  - Set priorities (Low, Medium, High)
  - Track status (Pending, In Progress, Completed)
  - Comment system for task discussions
  - Filter and sort tasks

- **Dashboard**
  - Visual statistics of task distribution
  - Progress tracking with interactive charts
  - Overdue task indicators

## Technology Stack

- **Backend**: Django 5.2
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: Bootstrap 5, jQuery
- **Authentication**: Django Auth, Social Auth (Google)
- **Testing**: Django Test Framework

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Kart0l/task-manager.git
   cd task-manager
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On Unix/MacOS
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file in the project root
   - Add the following variables (adjust as needed):
     ```
     # Generate a secure key with: python -c "import secrets; print(secrets.token_urlsafe(64))"
     SECRET_KEY=generate_a_reliable_key_min_50_characters
     DEBUG=True
     ALLOWED_HOSTS=localhost,127.0.0.1
     SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_oauth_key
     SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_oauth_secret
     ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application:
   - Web interface: http://localhost:8000
   - Admin interface: http://localhost:8000/admin

## Testing

Run the test suite to ensure everything is working correctly:

```bash
python manage.py test
```

For more detailed test output:

```bash
python manage.py test -v 2
```

## Project Structure

- **accounts/** - User authentication and profiles
- **tasks/** - Task creation, management, and comments
- **core/** - Shared functionality and utilities
- **templates/** - HTML templates organized by app
- **static/** - CSS, JavaScript, and images

## Development Guidelines

- Use the `.venv` virtual environment
- Run `flake8` before committing code
- Write tests for new features
- Update migrations with `python manage.py makemigrations`
- Keep documentation up-to-date

## Deployment

### Production Settings

For deploy in local:

1. Update your `.env` file with next settings:
   ```
   # Generate a secure key:
   # python -c "import secrets; print(secrets.token_urlsafe(64))"
   SECRET_KEY=your_secure_key_at_least_50_chars_long
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_key
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_secret
   ```

2. Static files:
   ```bash
   python manage.py collectstatic
   ```

3. Setup db:
   ```bash
   # Exaple for PostgreSQL in .env
   DATABASE_URL=postgres://user:password@localhost:5432/dbname
   ```

4. start Gunicorn:
   ```bash
   gunicorn task_manager.wsgi:application
   ```

5. Configuring Nginx for Query Proxies and HTTPS.

### Security Settings

For the production environment, we automatically enable the following security settings:

- HTTPS redirection (SECURE_SSL_REDIRECT)
- HTTP Strict Transport Security (SECURE_HSTS_SECONDS)
- Secure cookies for sessions (SESSION_COOKIE_SECURE)
- CSRF protection with safe cookies (CSRF_COOKIE_SECURE)
- Protection against XSS and content-type attacks


## License

[Specify your license here]

## Contributors

- [Kart0l](https://github.com/Kart0l/task_manager.git)

## Acknowledgements

- Django community
- Bootstrap team
- Django REST framework
- Crispy Forms
- Social Auth

## Access to the project

The project is deployed and available at the following link:
[EasyTask](https://easytask-300o.onrender.com/)

## Test Superuser Data

For testing, you can log in as an administrator using the following data:
Login: user
Password: user12345
 