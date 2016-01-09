# -*- coding: utf-8 -*-

from my_game.models import Flightplan
from my_game.flightplan.start import start_flight, start_colonization, start_extraction, start_refill, \
    start_repair_build, start_scaning, start_unload_hold, start_upload_hold


def starting_flight(*args):
    fleet = args[0]
    session_user = args[1]
    message = ''
    flightplan = Flightplan.objects.filter(fleet=fleet).first()
    if flightplan.class_command == 1:
        message = start_flight.start_flight(fleet)

    elif flightplan.class_command == 2:
        if flightplan.id_command == 1:
            message = start_upload_hold.start_upload(fleet)
        else:
            message = start_unload_hold.start_unload(fleet)

    elif flightplan.class_command == 3:
        message = start_extraction.start_extraction(fleet)

    elif flightplan.class_command == 4:
        message = start_refill.start_refill(session_user, fleet)

    elif flightplan.class_command == 5 or flightplan.class_command == 7:
        message = start_repair_build.start_repair_build(fleet)

    elif flightplan.class_command == 6:
        message = start_scaning.start_scaning(fleet)

    elif flightplan.class_command == 8:
        message = start_colonization.start_colonization(fleet)

    return message
