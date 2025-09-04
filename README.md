# Pestozap Backend API

A Django REST API backend for the Pestozap pest control application.

## Features

- **User Management**: Custom user model with profiles, authentication via JWT
- **Blog System**: Full-featured blog with categories, tags, comments, and likes
- **REST API**: Comprehensive API endpoints with filtering, search, and pagination
- **Admin Interface**: Django admin for content management
- **PostgreSQL**: Production-ready database
- **Security**: JWT authentication, CORS handling, input validation

## Tech Stack

- **Framework**: Django 4.2.7
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **Image Handling**: Pillow
- **CORS**: django-cors-headers
- **Filtering**: django-filter

## Project Structure

```
backend/
├── pestozap_backend/          # Main Django project
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── apps/                    # Django applications
│   ├── common/              # Common models and utilities
│   ├── users/               # User management
│   └── blog/                # Blog functionality
├── media/                   # User uploaded files
├── static/                  # Static files
├── logs/                    # Application logs
└── requirements.txt         # Python dependencies
```

## Setup Instructions

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Install PostgreSQL and create database
createdb pestozap_db

# Copy environment file
cp .env.example .env

# Update .env with your database credentials
```

### 3. Django Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/users/` - User registration
- `POST /api/v1/auth/jwt/create/` - Login (get JWT tokens)
- `POST /api/v1/auth/jwt/refresh/` - Refresh JWT token
- `POST /api/v1/auth/jwt/verify/` - Verify JWT token

### Users
- `GET /api/v1/users/profile/` - Get user profile
- `PUT /api/v1/users/profile/update/` - Update user profile
- `GET /api/v1/users/stats/` - Get user statistics

### Blog
- `GET /api/v1/blog/posts/` - List blog posts
- `GET /api/v1/blog/posts/{slug}/` - Get blog post detail
- `POST /api/v1/blog/posts/create/` - Create blog post (authenticated)
- `GET /api/v1/blog/categories/` - List categories
- `GET /api/v1/blog/tags/` - List tags
- `GET /api/v1/blog/posts/featured/` - Get featured posts
- `GET /api/v1/blog/posts/{slug}/comments/` - Get post comments
- `POST /api/v1/blog/posts/{slug}/comments/` - Add comment (authenticated)
- `POST /api/v1/blog/posts/{slug}/like/` - Toggle like (authenticated)

## Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=pestozap_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin Interface
Access the admin interface at `http://localhost:8000/admin/`

## Deployment

### Production Settings
- Set `DEBUG=False`
- Configure proper `ALLOWED_HOSTS`
- Use environment variables for sensitive data
- Set up proper media/static file serving
- Configure email backend for production

### Database
- Use PostgreSQL in production
- Set up database backups
- Configure connection pooling

### Security
- Use HTTPS in production
- Set secure cookie settings
- Configure CORS properly
- Use strong SECRET_KEY

## API Documentation

The API follows REST conventions:
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Return proper HTTP status codes
- Include pagination for list endpoints
- Support filtering and searching
- Provide detailed error messages

## Contributing

1. Follow PEP 8 style guidelines
2. Write tests for new features
3. Update documentation
4. Use meaningful commit messages