from django.db import models


class ServiceCharge(models.Model):
    service_type = models.CharField(max_length=32)
    charge_type = models.CharField(max_length=32)
    price = models.CharField(max_length=255)
    added_to_flight = models.BooleanField(default=False)


class Flight(models.Model):
    carrier = models.JSONField()

    flight_number = models.IntegerField()

    source = models.CharField(max_length=16)
    destination = models.CharField(max_length=16)

    departure_time_stamp = models.CharField(max_length=255)
    arrival_time_stamp = models.CharField(max_length=255)

    flight_class = models.CharField(max_length=16)
    number_of_stops = models.IntegerField()

    fare_basis = models.CharField(max_length=255)

    ticket_type = models.CharField(max_length=16)

    onward_ticket = models.BooleanField(default=False)
    return_ticket = models.BooleanField(default=False)

    added_to_flight = models.BooleanField(default=False)


class FlightPacket(models.Model):
    request_number = models.IntegerField()
    flights = models.ManyToManyField(Flight, blank=True)
    pricing_currency = models.CharField(max_length=16)
    service_charges = models.ManyToManyField(ServiceCharge)
