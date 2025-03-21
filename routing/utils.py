OFF_DUTY_STATUS = 'OFF'
SLEEPER_BERTH_DUTY_STATUS = 'SB'
DRIVING_DUTY_STATUS = 'D'
ON_DUTY_NOT_DRIVING_STATUS = 'ON'

DUTY_STATUS_CHOICES = [
        (OFF_DUTY_STATUS, 'Off Duty'),
        (SLEEPER_BERTH_DUTY_STATUS, 'Sleeper Berth'),
        (DRIVING_DUTY_STATUS, 'Driving'),
        (ON_DUTY_NOT_DRIVING_STATUS, 'On Duty Not Driving'),
    ]

PICKUP_STOP_TYPE = 'PICKUP'
DROP_OFF_STOP_TYPE = 'DROPOFF'
REST_STOP_TYPE = 'REST'
FUEL_STOP_TYPE = 'FUEL'

STOP_TYPE_CHOICES = [
        (REST_STOP_TYPE, 'Required Rest Stop'),
        (FUEL_STOP_TYPE, 'Fuel Stop'),
        (PICKUP_STOP_TYPE, 'Pickup Location'),
        (DROP_OFF_STOP_TYPE, 'Dropoff Location'),
    ]