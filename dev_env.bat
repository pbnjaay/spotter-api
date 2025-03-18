@echo off
REM Set development environment variables

REM Django settings
set SECRET_KEY=django-insecure-a7d+vts38jz5olou!p=oc9%%@05k(wta$b#p#5%%uedp&!0td1jr
set DEBUG=True
set ALLOWED_HOSTS=localhost,127.0.0.1

REM CORS settings
set CORS_ALLOW_ALL_ORIGINS=True
set CORS_ALLOWED_ORIGINS=http://localhost:3000

REM Run the server with these environment variables
echo Environment variables set for development.
echo Run 'python manage.py runserver' to start the server.
