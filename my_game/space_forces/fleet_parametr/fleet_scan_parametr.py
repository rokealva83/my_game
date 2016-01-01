# -*- coding: utf-8 -*-

from my_game.models import ModulePattern, FleetParametrScan, Ship, ElementShip


def fleet_scan_parametr(*args):
    fleet = args[0]
    ship_scan_elements = args[1]
    added_remove = args[2]
    if added_remove == 1:
        for ship_scan_element in ship_scan_elements:
            fleet_parametr_scan = FleetParametrScan.objects.filter(fleet=fleet,
                                                                   method_scanning=ship_scan_element.param3).first()
            if fleet_parametr_scan:
                if ship_scan_element.param1 > fleet_parametr_scan.range_scanning:
                    setattr(fleet_parametr_scan, 'time_scanning', ship_scan_element.param2)
                    setattr(fleet_parametr_scan, 'range_scanning', ship_scan_element.param1)
                    fleet_parametr_scan.save()
            else:
                fleet_parametr_scan = FleetParametrScan(
                    fleet=fleet,
                    method_scanning=ship_scan_element.param3,
                    time_scanning=ship_scan_element.param2,
                    range_scanning=ship_scan_element.param1,
                )
                fleet_parametr_scan.save()
    elif added_remove == -1:
        fleet_ships = Ship.objects.filter(fleet_status=1, place_id=fleet.id).all()
        scan_elements = []
        method = []
        for ship in fleet_ships:
            ship_elements = ElementShip.objects.filter(project_ship=ship.project_ship, class_element=8).all()
            for element in ship_elements:
                element_pattern = ModulePattern.objects.filter(id=element.element_pattern_id,
                                                               module_class=6).first()
                if element_pattern:
                    scan_elements.append(element_pattern)
                    method.append(element_pattern.param3)
        if scan_elements:
            fleet_parametr_scans = FleetParametrScan.objects.filter(fleet=fleet).all()
            for fleet_parametr_scan in fleet_parametr_scans:
                if fleet_parametr_scan.method_scanning not in list(set(method)):
                    FleetParametrScan.objects.filter(id=fleet_parametr_scan.id).delete()
                else:
                    for scan_element in scan_elements:
                        if scan_element.param3 == fleet_parametr_scan.method_scanning and (
                                    scan_element.param1 > fleet_parametr_scan.range_scanning):
                            setattr(fleet_parametr_scan, 'time_scanning', element_pattern.param2)
                            setattr(fleet_parametr_scan, 'range_scanning', element_pattern.param1)
                            fleet_parametr_scan.save()
        else:
            FleetParametrScan.objects.filter(fleet=fleet).delete()

    return True
