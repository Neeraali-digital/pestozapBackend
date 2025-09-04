@echo off
echo Setting up Pestozap Backend for development...

REM Check if .env exists
if not exist .env (
    if exist .env.example (
        echo Creating .env from .env.example...
        copy .env.example .env
        echo .env file created
    ) else (
        echo .env.example not found
        pause
        exit /b 1
    )
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

REM Run migrations
echo Creating migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Failed to create migrations
    pause
    exit /b 1
)

echo Running migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Failed to run migrations
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Create a superuser: python manage.py createsuperuser
echo 2. Run the server: python manage.py runserver
echo 3. Visit: http://localhost:8000/admin/
echo.
pause