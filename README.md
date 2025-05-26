# Flask Application Template

A comprehensive template for building Flask applications with built-in support for authentication, admin panel, database management, and rate limiting.

## Features

- **Authentication System**
  - JWT-based authentication
  - Google OAuth integration
  - HTTP Basic Auth support
  - Role-based access control

- **Admin Panel**
  - Customizable admin interface using Flask-Admin
  - Database management through the admin UI
  - Custom admin views

- **Database Support**
  - SQLAlchemy ORM integration
  - Database migrations using Flask-Migrate
  - MySQL support (configurable for other databases)

- **API Development**
  - RESTful API structure with Flask-RESTX
  - Swagger documentation
  - Custom request parsers
  - Standardized error handling

- **Security Features**
  - Rate limiting with Flask-Limiter
  - CORS protection
  - Environment-based configuration

## Project Structure

```
flask-template/
├── app/                    # Main application package
│   ├── admin/              # Admin panel configuration
│   ├── models/             # Database models
│   ├── routes/             # API routes and endpoints
│   ├── resources/          # API resources and business logic
│   ├── __init__.py         # Application factory
│   ├── extensions.py       # Flask extensions
│   └── settings.py         # Application settings
├── migrations/             # Database migration files
├── .env                    # Environment variables (local)
├── .env.example            # Example environment variables
├── poetry.lock             # Poetry dependencies lock file
└── pyproject.toml          # Project dependencies and metadata
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- MySQL (or alternative database)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flask-template.git
   cd flask-template
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```bash
   poetry run flask db init
   poetry run flask db migrate -m "Initial migration"
   poetry run flask db upgrade
   ```

5. Run the development server:
   ```bash
   poetry run flask run --debug
   ```

## Configuration

The application can be configured using environment variables in the `.env` file:

- `APP_ENVIRONMENT`: Set to "development", "testing", or "production"
- `SECRET_KEY`: Secret key for securing the application
- `DATABASE_URI`: Database connection string
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- And more...

## Deployment

For production deployment:

1. Set `APP_ENVIRONMENT=production` in your environment
2. Configure a production-ready web server (Gunicorn, uWSGI)
3. Set up a reverse proxy (Nginx, Apache)
4. Configure proper database credentials
5. Set up proper logging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
