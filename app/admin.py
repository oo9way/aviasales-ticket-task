from django.contrib import admin

from app.models import ServiceCharge, Flight, FlightPacket

# Register your models here.

admin.site.register([ServiceCharge, Flight, FlightPacket])
