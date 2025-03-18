$env:SECRET_KEY = "django-insecure-a7d+vts38jz5olou!p=oc9%@05k(wta$b#p#5%uedp&!0td1jr"
$env:DEBUG = "True"
$env:ALLOWED_HOSTS = "localhost,127.0.0.1"

$env:CORS_ALLOW_ALL_ORIGINS = "True"
$env:CORS_ALLOWED_ORIGINS = "http://localhost:3000"

Write-Host "Environment variables set for development."
Write-Host "Run 'python manage.py runserver' to start the server."
