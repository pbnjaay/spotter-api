# Spotter API

Django REST API for the Spotter application.

## Deployment to Railway

### Prerequisites

- A [Railway](https://railway.app/) account
- [Railway CLI](https://docs.railway.app/develop/cli) (optional)

### Deployment Steps

1. **Create a new project in Railway**

   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"

2. **Connect your GitHub repository**

   - Select the repository containing this API
   - Railway will automatically detect the Django project

3. **Set up environment variables**

   Create the following environment variables in Railway dashboard:

   - `SECRET_KEY`: A secure random string
   - `DEBUG`: Set to "False" for production
   - `ALLOWED_HOSTS`: Add your Railway domain (e.g., `.railway.app`)
   - `CORS_ALLOW_ALL_ORIGINS`: Set to "False" for production
   - `CORS_ALLOWED_ORIGINS`: Add your frontend URL(s)

4. **Add a PostgreSQL database**

   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set the `DATABASE_URL` environment variable

5. **Deploy your application**

   - Railway will automatically deploy your application
   - You can trigger manual deployments from the dashboard

### Local Development After Railway Setup

1. Copy `.env.example` to `.env` and update the values
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

### Quick Start Development Environment

For convenience, several scripts are provided to set up the development environment:

#### Windows Command Prompt
``` 
dev_env.bat
python manage.py runserver
```

#### PowerShell
``` 
.\dev_env.ps1
python manage.py runserver
```

#### Python Script (Cross-platform)
``` 
python run_dev_server.py
```

## API Documentation

[Add your API documentation here]
