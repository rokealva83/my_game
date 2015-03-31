# -*- coding: utf-8 -*-

import random
from datetime import datetime, timedelta

from django.utils import timezone
import math
from my_game.models import Planet
from my_game.models import MyUser, User_city, User_scientic, System, Asteroid_field
from my_game.models import Turn_scientic, Turn_building, Turn_assembly_pieces, \
    Turn_production
from my_game.models import Factory_pattern, Factory_installed, Building_pattern, Building_installed
from my_game.models import Warehouse_factory, Warehouse_element, Warehouse
from knowledge import scientic_func
from my_game.models import Project_ship, Turn_ship_build, Ship, Fleet, Element_ship, Hold
from my_game.models import Flightplan, Flightplan_flight, Fleet_parametr_scan
from my_game.models import Trade_flight, Trade_teleport
from my_game.models import User_variables ,Mail


def verification_flight_list(request):
    user = request
    fleets = Fleet.objects.filter(user=user)
    for fleet in fleets:
        flightplans = Flightplan.objects.filter(id_fleet=fleet.id)
        flightplan_len = len(flightplans)
        lens = 0
        for flightplan in flightplans:
            if flightplan.status == 1:
                if flightplan.class_command == 1:
                    flightplan_flight = Flightplan_flight.objects.filter(id_fleetplan=flightplan.id).first()
                    flightplan_id = int(flightplan.id)
                    time = timezone.now()
                    time_start = flightplan_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = flightplan_flight.flight_time
                    if new_delta > delta:
                        if flightplan_flight.planet != 0:
                            planet_status = 1
                            planet = Planet.objects.filter(system_id=flightplan_flight.system,
                                                           planet_num=flightplan_flight.planet).first()
                            x = planet.x
                            y = planet.y
                            z = planet.z

                        else:
                            planet_status = 0
                            x = flightplan_flight.finish_x / 1000.0
                            y = flightplan_flight.finish_y / 1000.0
                            z = flightplan_flight.finish_z / 1000.0

                        fleet_up = Fleet.objects.filter(id=fleet.id).update(x=x, y=y, z=z, planet_status=planet_status,
                                                                            planet=flightplan_flight.planet,
                                                                            system=flightplan_flight.system)

                        old_flightplan_flight = flightplan_flight
                        flightplan_flight = Flightplan_flight.objects.filter(id_fleetplan=flightplan.id).delete()
                        flightplan = Flightplan.objects.filter(id=flightplan_id).delete()

                elif flightplan.class_command == 6:
                    if flightplan.id_command == 1:
                        system = System.objects.filter(id=fleet.system).first()
                        fleet_parametr_scan = Fleet_parametr_scan.objects.filter(fleet_id = fleet.id, method_scanning = flightplan.id_command).first()

                        if fleet.planet_status == 1:
                            fleet_x = (int(system.x) * 1000 + int(fleet.x)) / 1000.0
                            fleet_y = (int(system.y) * 1000 + int(fleet.y)) / 1000.0
                            fleet_z = (int(system.z) * 1000 + int(fleet.z)) / 1000.0
                        else:
                            fleet_x = int(fleet.x)
                            fleet_y = int(fleet.y)
                            fleet_z = int(fleet.z)

                        delta = fleet_parametr_scan.range_scanning
                        max_x = fleet_x + delta
                        min_x = fleet_x - delta
                        max_y = fleet_y + delta
                        min_y = fleet_y - delta
                        max_z = fleet_z + delta
                        min_z = fleet_z - delta
                        systems = System.objects.filter()
                        asteroid_fields = Asteroid_field.objects.filter()
                        mail = 'Координаты систем:' + '\n'
                        for system in systems:
                            if min_x <= system.x <= max_x and min_y <= system.y <= max_y and min_z <= system.z <= max_z:
                                system_x = system.x
                                system_y = system.y
                                system_z = system.z
                                distance = round(math.sqrt(
                                    (fleet_x - system_x) ** 2 + (fleet_y - system_y) ** 2 + (fleet_z - system_z) ** 2), 3)
                                if distance <= delta and distance != 0:
                                    line = str(system_x) + ':' + str(system_y) + ':' + str(system_z) + ' Растояние:' + str(
                                        distance) + ' св.' + ' \n'
                                    mail = mail + line

                        size = 0
                        ast_mail = '\n'+ 'Координаты астероидных полей:' + '\n'
                        for asteroid_field in asteroid_fields:
                            if min_x <= asteroid_field.x <= max_x and min_y <= asteroid_field.y <= max_y and min_z <= asteroid_field.z <= max_z:
                                system_x = asteroid_field.x
                                system_y = asteroid_field.y
                                system_z = asteroid_field.z
                                asteroid_size = asteroid_field.size
                                size = size + asteroid_field.size
                                distance = round(math.sqrt(
                                    (fleet_x - system_x) ** 2 + (fleet_y - system_y) ** 2 + (fleet_z - system_z) ** 2), 3)
                                if distance <= delta:
                                    line = str(system_x) + ' : ' + str(system_y) + ' : ' + str(system_z) + ' (' + str(
                                        asteroid_size) + ') ' + ' Растояние:' + str(distance) + ' св.' + '\n'
                                    ast_mail = ast_mail + line
                        final_mail = mail + '\n' +ast_mail

                    mail = Mail(
                        user = user,
                        recipient = 0,
                        time = datetime.now(),
                        status = 1,
                        category = 4,
                        login_recipient = 'Система',
                        title = 'Отчет сканирования',
                        message = final_mail
                    )


            lens = lens + 1
            if lens == flightplan_len:
                fleet_up = Fleet.objects.filter(id=fleet.id).update(status=0)
            else:
                flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first().update(status=1)
