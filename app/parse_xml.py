import xml.etree.ElementTree as ET
from django.conf import settings
from app.models import FlightPacket, Flight, ServiceCharge
from datetime import datetime


def parse_xml(path, request_number):
    tree = ET.parse(path)
    root = tree.getroot()

    flights = root[1]

    for packet in flights:
        pricing_currency = packet[-1].attrib["currency"]

        service_charges = []

        for service_charge in packet[-1]:
            service_charges.append(
                ServiceCharge(
                    service_type=service_charge.attrib["type"],
                    charge_type=service_charge.attrib["ChargeType"],
                    price=service_charge.text,
                )
            )

        # How to bulk through FlightPacket model

        flight_packet = FlightPacket(
            request_number=request_number, pricing_currency=pricing_currency
        )

        onward_flights = packet[0]
        try:
            return_flights = packet[1]
        except IndexError:
            return_flights = []

        tickets = []

        for onward_flight in onward_flights[0]:
            carrier = {
                "unique_name": onward_flight[0].attrib["id"],
                "name": onward_flight[0].text,
            }
            flight = Flight(
                carrier=carrier,
                flight_number=onward_flight[1].text,
                source=onward_flight[2].text,
                destination=onward_flight[3].text,
                departure_time_stamp=onward_flight[4].text,
                arrival_time_stamp=onward_flight[5].text,
                flight_class=onward_flight[6].text,
                number_of_stops=onward_flight[7].text,
                fare_basis=onward_flight[8].text,
                ticket_type=onward_flight[10].text,
                onward_ticket=True,
            )

            tickets.append(flight)

        for return_flight in return_flights[0]:
            carrier = {
                "unique_name": return_flight[0].attrib["id"],
                "name": return_flight[0].text,
            }
            flight = Flight(
                carrier=carrier,
                flight_number=return_flight[1].text,
                source=return_flight[2].text,
                destination=return_flight[3].text,
                departure_time_stamp=return_flight[4].text,
                arrival_time_stamp=return_flight[5].text,
                flight_class=return_flight[6].text,
                number_of_stops=return_flight[7].text,
                fare_basis=return_flight[8].text,
                ticket_type=return_flight[10].text,
                return_ticket=True,
            )

            tickets.append(flight)

        ServiceCharge.objects.bulk_create(service_charges)
        Flight.objects.bulk_create(tickets)

        tickets = Flight.objects.filter(added_to_flight=False)
        service_charges = ServiceCharge.objects.filter(added_to_flight=False)

        flight_packet.save()
        flight_packet.flights.add(*tickets)
        flight_packet.service_charges.add(*service_charges)

        tickets.update(added_to_flight=True)
        service_charges.update(added_to_flight=True)


path1 = settings.BASE_DIR / "files/aviasales.xml"
path2 = settings.BASE_DIR / "files/aviasales2.xml"

parse_xml(path1, 1)
parse_xml(path2, 2)
