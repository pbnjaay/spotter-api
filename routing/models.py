from django.db import models
from .utils import DUTY_STATUS_CHOICES, STOP_TYPE_CHOICES

class Trip(models.Model):
    current_location = models.JSONField(help_text='Current location coordinates {lat: float, lng: float}')
    pickup_location = models.JSONField(help_text='Pickup location coordinates {lat: float, lng: float}')
    dropoff_location = models.JSONField(help_text='Dropoff location coordinates {lat: float, lng: float}')
    current_cycle_hours = models.FloatField(help_text='Current cycle hours used')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class RouteStop(models.Model):
    trip = models.ForeignKey(Trip, related_name='stops', on_delete=models.CASCADE)
    location = models.JSONField(help_text='Stop location coordinates {lat: float, lng: float}')
    stop_type = models.CharField(max_length=20, choices=STOP_TYPE_CHOICES)
    planned_arrival = models.DateTimeField()
    planned_departure = models.DateTimeField()
    sequence = models.IntegerField(help_text='Stop sequence in the route')
    
    class Meta:
        ordering = ['planned_arrival']

class ELDLog(models.Model):
    trip = models.ForeignKey(Trip, related_name='eld_logs', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duty_status = models.CharField(max_length=3, choices=DUTY_STATUS_CHOICES)
    location = models.JSONField(help_text='Location coordinates {lat: float, lng: float}')
    remarks = models.TextField(blank=True)
