# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import Fleet
from my_game.models import Flightplan
from my_game.flightplan.start import start_flight, start_extraction, start_refill, start_scaning, start_unload_hold, \
    start_upload_hold
from my_game.flightplan.veryfication.flight_verification import verification_flight
from my_game.flightplan.veryfication.scan_veryfication import scan_veryfication
from my_game.flightplan.veryfication.extraction_veryfication import extraction_veryfication
from my_game.flightplan.veryfication.upload_unload_veryfication import upload_unload_veryfication
from my_game.flightplan.veryfication.colonization_veryfication import colonization_veryfication


def verification_flight_list(request):
    user = request
    fleets = Fleet.objects.filter(user=user)
    finish_time = timezone.now()
    for fleet in fleets:
        flightplans = Flightplan.objects.filter(fleet=fleet)
        for flightplan in flightplans:
            if flightplan.status == 1:
                if flightplan.class_command == 1:
                    finish_time = verification_flight(fleet)
                    flightplan = Flightplan.objects.filter(fleet=fleet, status=0).first()

                elif flightplan.class_command == 2:
                    finish_time = upload_unload_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(fleet=fleet, status=0).first()

                elif flightplan.class_command == 3:
                    finish_time = extraction_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(fleet=fleet, status=0).first()

                elif flightplan.class_command == 6:
                    finish_time = scan_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(fleet=fleet, status=0).first()

                elif flightplan.class_command == 8:
                    finish_time = colonization_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(fleet=fleet, status=0).first()

                if flightplan:
                    if flightplan.class_command == 1:
                        start_flight.start_flight(fleet, finish_time)

                    elif flightplan.class_command == 2:
                        if flightplan.command_id == 1:
                            start_upload_hold.start_upload(fleet, finish_time)
                        else:
                            start_unload_hold.start_unload(fleet, finish_time)

                    elif flightplan.class_command == 3:
                        start_extraction.start_extraction(fleet, finish_time)

                    elif flightplan.class_command == 4:
                        start_refill.start_refill(user, fleet, finish_time)

                    elif flightplan.class_command == 6:
                        start_scaning.start_scaning(fleet, finish_time)
                else:
                    Fleet.objects.filter(id=fleet.id).update(status=0)
