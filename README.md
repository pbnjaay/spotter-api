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

### Trip Endpoints

#### Create Trip

- **URL**: `/api/trips/`
- **Method**: `POST`
- **Description**: Creates a new trip with automatic route planning, stop generation, and ELD log creation
- **Request Body**:
  ```json
  {
    "current_location": {
      "lat": 37.7749,
      "lng": -122.4194
    },
    "pickup_location": {
      "lat": 34.0522,
      "lng": -118.2437
    },
    "dropoff_location": {
      "lat": 32.7157,
      "lng": -117.1611
    },
    "current_cycle_hours": 0
  }
  ```
- **Response**: Returns the created trip with all stops and ELD logs

#### Get All Trips

- **URL**: `/api/trips/`
- **Method**: `GET`
- **Description**: Returns a list of all trips
- **Response**: List of trip objects with their stops and ELD logs

#### Get Trip Details

- **URL**: `/api/trips/{id}/`
- **Method**: `GET`
- **Description**: Returns details for a specific trip
- **Response**: Trip object with all stops and ELD logs

#### Update Trip

- **URL**: `/api/trips/{id}/`
- **Method**: `PUT`
- **Description**: Updates a trip (note: this will not regenerate stops or ELD logs)
- **Request Body**: Same as create trip

#### Delete Trip

- **URL**: `/api/trips/{id}/`
- **Method**: `DELETE`
- **Description**: Deletes a trip and all associated stops and ELD logs

### Route Planning Logic

The API automatically plans routes using the following logic:

1. Calculates the optimal route between current location, pickup, and dropoff using OSRM
2. Adds required rest stops based on Hours of Service (HOS) regulations:
   - 11-hour driving limit
   - 14-hour on-duty limit
   - 30-minute break after 8 hours of driving
   - 70-hour/8-day limit (with 34-hour restart)
3. Adds fuel stops approximately every 1000 miles
4. Generates ELD logs for the entire trip

