from django.shortcuts import render
from django.views.generic import ListView

from app.models import FlightPacket


class AviaSalesHome(ListView):
    queryset = FlightPacket.objects.all()
    paginate_by = 20
    template_name = "index.html"

    def get_queryset(self):
        # Get the new and old tickets separately
        new_tickets = FlightPacket.objects.filter(request_number=1)
        old_tickets = FlightPacket.objects.filter(request_number=2)

        combined_tickets = []

        # Interleave the new and old tickets in the desired order
        for i in range(0, max(len(new_tickets), len(old_tickets)), 2):
            if i < len(old_tickets):
                combined_tickets.append(old_tickets[i])
            if i < len(new_tickets):
                combined_tickets.append(new_tickets[i])

        print(len(combined_tickets))

        return combined_tickets
