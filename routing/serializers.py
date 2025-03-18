from rest_framework import serializers
from .models import Trip, RouteStop, ELDLog

class LocationField(serializers.JSONField):
    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("Location must be an object with 'lat' and 'lng' fields")
        if 'lat' not in data or 'lng' not in data:
            raise serializers.ValidationError("Location must contain both 'lat' and 'lng' fields")
        try:
            lat = float(data['lat'])
            lng = float(data['lng'])
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                raise serializers.ValidationError("Invalid latitude or longitude values")
        except (TypeError, ValueError):
            raise serializers.ValidationError("Latitude and longitude must be numbers")
        return data

class RouteStopSerializer(serializers.ModelSerializer):
    location = LocationField()
    
    class Meta:
        model = RouteStop
        fields = '__all__'

class ELDLogSerializer(serializers.ModelSerializer):
    location = LocationField()
    
    class Meta:
        model = ELDLog
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    current_location = LocationField()
    pickup_location = LocationField()
    dropoff_location = LocationField()
    stops = RouteStopSerializer(many=True, read_only=True)
    eld_logs = ELDLogSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'

class TripCreateSerializer(serializers.ModelSerializer):
    current_location = LocationField()
    pickup_location = LocationField()
    dropoff_location = LocationField()

    class Meta:
        model = Trip
        fields = ['current_location', 'pickup_location', 'dropoff_location', 'current_cycle_hours']
