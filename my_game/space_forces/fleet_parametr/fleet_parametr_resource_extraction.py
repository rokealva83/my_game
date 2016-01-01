# -*- coding: utf-8 -*-

from my_game.models import FleetParametrResourceExtraction


def fleet_parametr_resource_extraction(*args):
    fleet = args[0]
    ship_extraction_elements = args[1]
    ship_amount = args[2]
    extraction_ship = 0
    for ship_extraction_element in ship_extraction_elements:
        extraction_ship += ship_extraction_element.param1
    extraction_ships = extraction_ship * ship_amount * args[3]
    if extraction_ship:
        fleet_extraction = FleetParametrResourceExtraction.objects.filter(fleet=fleet).first()
        if fleet_extraction:
            new_extraction = fleet_extraction.extraction_per_minute + extraction_ships
            setattr(fleet_extraction, 'extraction_per_minute', new_extraction)
            fleet_extraction.save()
        else:
            fleet_extraction = FleetParametrResourceExtraction(
                fleet=fleet,
                extraction_per_minute=extraction_ships)
            fleet_extraction.save()
    return True
