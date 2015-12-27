# -*- coding: utf-8 -*-

from my_game.models import Hold
from my_game.flightplan.veryfication.hold_unload import hold_unload


def unload_hold_element(*args):
    fleet = args[0]
    flightplan = args[1]
    flightplan_hold = args[2]
    city = args[3]

    if flightplan.id_command == 2:
        hold = Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                   id_shipment=flightplan_hold.id_element).first()
        if hold:
            hold_unload(fleet, flightplan, flightplan_hold, city, hold)
        else:
            message = 'В трюме нет такого модуля'
            return message
    elif flightplan.id_command == 3:
        hold = Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                   id_shipment=flightplan_hold.id_element).first()
        if hold:
            hold_unload(fleet, flightplan, flightplan_hold, city, hold)
        else:
            message = 'В трюме нет такого модуля'
            return message
    elif flightplan.id_command == 4:
        holds = Hold.objects.filter(fleet_id=fleet.id)
        for hold in holds:
            hold_unload(fleet, flightplan, flightplan_hold, city, hold)
        return True
