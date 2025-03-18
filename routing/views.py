from datetime import timedelta

import requests
from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import ELDLog, RouteStop, Trip
from .serializers import TripCreateSerializer, TripSerializer
from .utils import (DRIVING_DUTY_STATUS, DROP_OFF_STOP_TYPE, FUEL_STOP_TYPE,
                    ON_DUTY_NOT_DRIVING_STATUS, PICKUP_STOP_TYPE,
                    REST_STOP_TYPE, SLEEPER_BERTH_DUTY_STATUS)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_serializer_class(self):
        return TripCreateSerializer if self.action == 'create' else TripSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()

        try:
            route_data = self._calculate_route(trip)
            if route_data and route_data.get('routes'):
                self._create_stops(trip, route_data)
                self._generate_eld_logs(trip)
                return Response(TripSerializer(trip).data, status=status.HTTP_201_CREATED)
            else:
                trip.delete()
                return Response({'error': 'Invalid route data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            trip.delete()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def _calculate_route(self, trip):
        base_url = "http://router.project-osrm.org/route/v1/driving/"
        coords = [
            f"{trip.current_location['lng']},{trip.current_location['lat']}",
            f"{trip.pickup_location['lng']},{trip.pickup_location['lat']}",
            f"{trip.dropoff_location['lng']},{trip.dropoff_location['lat']}"
        ]
        url = base_url + ";".join(coords)
        params = {'overview': 'full', 'steps': 'true', 'geometries': 'geojson'}
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception("Failed to calculate route")
        return response.json()
    
    def _create_stops(self, trip, route_data):
        with transaction.atomic():
            legs = route_data['routes'][0]['legs']
            sequence = 1
            now = timezone.now()
            current_time = now
            duty_start_time = now
            
            driving_hrs = 0
            on_duty_hrs = 0
            historical_on_duty_hrs = trip.current_cycle_hours
            has_taken_30_min_break = False
            distance_traveled = 0
            
            for leg_index, leg in enumerate(legs):
                for step in leg['steps']:
                    step_duration = step['duration']
                    step_duration_hrs = step_duration / 3600
                    step_distance_miles = step['distance'] / 1609.34
                    coords = step['geometry']['coordinates']
                    
                    if not coords:
                        continue
                    
                    if (historical_on_duty_hrs + on_duty_hrs + step_duration_hrs) >= 70:
                        self._create_stop(
                            trip, {"lat": coords[0][1], "lng": coords[0][0]}, REST_STOP_TYPE,
                            current_time, sequence,
                            duration=timedelta(hours=34)
                        )
                        current_time += timedelta(hours=34)
                        sequence += 1
                        
                        historical_on_duty_hrs = 0
                        on_duty_hrs = 0
                        driving_hrs = 0
                        duty_start_time = current_time

                    if driving_hrs + step_duration_hrs >= 8 and not has_taken_30_min_break:
                        self._create_stop(
                            trip, {"lat": coords[0][1], "lng": coords[0][0]}, REST_STOP_TYPE,
                            current_time, sequence,
                            duration=timedelta(minutes=30)
                        )
                        current_time += timedelta(minutes=30)
                        sequence += 1
                        has_taken_30_min_break = True
                        on_duty_hrs += 0.5

                    elapsed_time = current_time - duty_start_time
                    if elapsed_time + timedelta(hours=step_duration_hrs) > timedelta(hours=14):
                        self._create_stop(
                            trip, {"lat": coords[0][1], "lng": coords[0][0]}, REST_STOP_TYPE,
                            current_time, sequence,
                            duration=timedelta(hours=10)
                        )
                        current_time += timedelta(hours=10)
                        sequence += 1
                        driving_hrs = 0
                        duty_start_time = current_time

                    if driving_hrs + step_duration_hrs >= 11:
                        self._create_stop(
                            trip, {"lat": coords[0][1], "lng": coords[0][0]}, REST_STOP_TYPE,
                            current_time, sequence,
                            duration=timedelta(hours=10)    
                        )
                        current_time += timedelta(hours=10)
                        sequence += 1
                        driving_hrs = 0
                        duty_start_time = current_time

                    if distance_traveled + step_distance_miles >= 1000:
                        self._create_stop(
                            trip, {"lat": coords[0][1], "lng": coords[0][0]}, FUEL_STOP_TYPE,
                            current_time, sequence,
                            duration=timedelta(minutes=30)
                        )
                        current_time += timedelta(minutes=30)
                        sequence += 1
                        distance_traveled = 0
                        on_duty_hrs += 0.5


                    driving_hrs += step_duration_hrs
                    on_duty_hrs += step_duration_hrs
                    distance_traveled += step_distance_miles
                    current_time += timedelta(seconds=step_duration)

                if leg_index == 0:
                    self._create_stop(
                        trip, trip.pickup_location, PICKUP_STOP_TYPE,
                        current_time, sequence,
                        duration=timedelta(hours=1)
                    )
                    current_time += timedelta(hours=1)
                    sequence += 1
                    on_duty_hrs += 1 
                else:
                    self._create_stop(
                        trip, trip.dropoff_location, DROP_OFF_STOP_TYPE,
                        current_time, sequence,
                        duration=timedelta(hours=1)
                    )

    def _create_stop(self, trip, location, stop_type, start_time, sequence, duration):
        RouteStop.objects.create(
            trip=trip,
            location=location,
            stop_type=stop_type,
            planned_arrival=start_time,
            planned_departure=start_time + duration,
            sequence=sequence
        )

    def _generate_eld_logs(self, trip):
        stops = trip.stops.all().order_by('sequence')
        for i, current_stop in enumerate(stops):
            duty_status, remarks = self._get_duty_status_and_remarks(current_stop)
            ELDLog.objects.create(
                trip=trip,
                start_time=current_stop.planned_arrival,
                end_time=current_stop.planned_departure,
                location=current_stop.location,
                duty_status=duty_status,
                remarks=remarks
            )

            if i < len(stops) - 1:
                next_stop = stops[i + 1]
                ELDLog.objects.create(
                    trip=trip,
                    start_time=current_stop.planned_departure,
                    end_time=next_stop.planned_arrival,
                    location=current_stop.location,
                    duty_status=DRIVING_DUTY_STATUS,
                    remarks=f"Driving to {next_stop.get_stop_type_display()}"
                )

    def _get_duty_status_and_remarks(self, stop):
        if stop.stop_type == REST_STOP_TYPE:
            return SLEEPER_BERTH_DUTY_STATUS, "Required rest period"
        elif stop.stop_type in [PICKUP_STOP_TYPE, DROP_OFF_STOP_TYPE, FUEL_STOP_TYPE]:
            return ON_DUTY_NOT_DRIVING_STATUS, f"{stop.get_stop_type_display()}"
        return None, None