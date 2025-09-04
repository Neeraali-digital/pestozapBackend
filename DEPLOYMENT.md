# Deployment Guide

## Production Checklist

Before deploying to production, ensure you:

### Security Settings
- [ ] Set `DEBUG=False` in production
- [ ] Generate a strong `SECRET_KEY` (50+ characters)
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up HTTPS and SSL certificates
- [ ] Configure secure cookies:
  - `SESSION_COOKIE_SECURE=True`
  - `CSRF_COOKIE_SECURE=True`
  - `SECURE_SSL_REDIRECT=True`
  - `SECURE_HSTS_SECONDS=31536000`

### Database
- [ ] Set up PostgreSQL database
- [ ] Configure database credentials in `.env`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`

### Static Files
- [ ] Run: `python manage.py collectstatic`
- [ ] Configure web server to serve static files

### Email Configuration
- [ ] Configure SMTP settings for email functionality
- [ ] Test email sending

### Environment Variables
Create a production `.env` file with:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=pestozap_prod
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_HOST=your_db_host
DB_PORT=5432

EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Deployment Options

### 1. Traditional Server (Ubuntu/CentOS)
- Install Python 3.11+, PostgreSQL, Nginx
- Use Gunicorn as WSGI server
- Configure Nginx as reverse proxy

### 2. Docker
- Use provided `Dockerfile` and `docker-compose.yml`
- Build and run containers

### 3. Cloud Platforms
- **Heroku**: Use `Procfile` and configure add-ons
- **AWS**: Use Elastic Beanstalk or EC2
- **DigitalOcean**: Use App Platform or Droplets

## Monitoring
- Set up logging and monitoring
- Configure error tracking (e.g., Sentry)
- Set up database backups