# -*- coding: utf-8 -*-

from django.utils import timezone
from datetime import timedelta
import math
from my_game.models import Planet
from my_game.models import System, AsteroidField, FlightplanScan
from my_game.models import Fleet, Ship
from my_game.models import Flightplan, FleetParametrScan
from my_game.models import Mail
from my_game.flightplan.veryfication.flight_verification import verification_flight
from my_game.flightplan.need_fuel_process import need_fuel_process
from my_game.flightplan.minus_fuel import minus_fuel


def scan_veryfication(*args):
    fleet = args[0]
    user = fleet.user
    flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first()

    mail_subject = ''
    final_mail = ''
    flightplan_scan = FlightplanScan.objects.filter(id_fleetplan=flightplan.id).first()
    if flightplan_scan:
        time = timezone.now()
        time_start = flightplan_scan.start_time
        delta_time = time - time_start
        new_delta = delta_time.total_seconds()
        delta = flightplan_scan.time_scanning
        if new_delta > delta:
            finish_time = time_start + timedelta(seconds=delta)
            fleet_parametr_scan = FleetParametrScan.objects.filter(fleet_id=fleet.id,
                                                                   method_scanning=flightplan.id_command).first()
            fleet_x = int(fleet.x)
            fleet_y = int(fleet.y)
            fleet_z = int(fleet.z)

            delta = int(fleet_parametr_scan.range_scanning) * 1000
            max_x = fleet_x + delta
            min_x = fleet_x - delta
            max_y = fleet_y + delta
            min_y = fleet_y - delta
            max_z = fleet_z + delta
            min_z = fleet_z - delta

            if flightplan.id_command == 1:
                systems = System.objects.all()
                mail_subject = u'Сканирование пространства'
                mail_text = u'Флот произвел сканирование пространства, находясь на координатам %s : %s : %s. \n  ' \
                            u'Координаты систем: \n' % (fleet_x, fleet_y, fleet_z)
                message_planet = u''
                for system in systems:
                    if min_x <= system.x <= max_x and min_y <= system.y <= max_y and min_z <= system.z <= max_z:
                        system_x = int(system.x)
                        system_y = int(system.y)
                        system_z = int(system.z)
                        distance = int(
                            math.sqrt(
                                (fleet_x - system_x) ** 2 + (fleet_y - system_y) ** 2 + (fleet_z - system_z) ** 2))
                        if distance <= delta and distance != 0:
                            line = u'    №%s. %s : %s : %s - растояние: %s св. \n' % (
                                system.id, system_x, system_y, system_z, int(distance / 1000))
                            if distance <= delta * 0.1:
                                message_planet_subject = u'      В системе найдены планеты с координатами: \n'
                                planets = Planet.objects.filter(system_id=system.id).order_by('planet_num')
                                for planet in planets:
                                    mess_planet = u'        №%s - %s : %s : %s \n' % (
                                        planet.planet_num, planet.global_x, planet.global_y, planet.global_z)
                                    message_planet += mess_planet
                                line = line + message_planet_subject + message_planet
                            mail_text += line
                final_mail = mail_text

            elif flightplan.id_command == 2:
                asteroid_fields = AsteroidField.objects.all()
                size = 0
                mail_subject = u'Поиск астероидных полей \n'
                ast_mail = u'Флот произвел поиск астероидов, находясь на координатам %s : %s : %s.\n  ' \
                           u'Координаты астероидных полей: \n' % (fleet_x, fleet_y, fleet_z)
                for asteroid_field in asteroid_fields:
                    if min_x <= asteroid_field.x <= max_x and min_y <= asteroid_field.y <= max_y and min_z <= (
                                asteroid_field.z <= max_z):
                        system_x = int(asteroid_field.x)
                        system_y = int(asteroid_field.y)
                        system_z = int(asteroid_field.z)
                        asteroid_size = asteroid_field.size
                        size += asteroid_field.size
                        distance = int(
                            math.sqrt(
                                (fleet_x - system_x) ** 2 + (fleet_y - system_y) ** 2 + (fleet_z - system_z) ** 2))
                        if distance <= delta:
                            line = u'    %s : %s : %s  Размер:%s Растояние:%s св. \n' % (
                                system_x, system_y, system_z, asteroid_size, int(distance / 1000))
                            ast_mail += line
                size = u'\nОбщий размер найденных полей: %s' % (size,)
                final_mail = ast_mail + size

            elif flightplan_scan.id_command == 3:
                fleets = Fleet.objects.filter(status=1)

                for fleet in fleets:
                    verification_flight(fleet)
                fleets = Fleet.objects.all()
                mail_subject = u'Сканирование пространства \n'
                fleet_mail = u'Флот произвел сканирование, находясь на координатам %s : %s : %s.\n  ' \
                             u'Координаты найденых флотов: \n' % (fleet_x, fleet_y, fleet_z)
                for fleet in fleets:
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first()
                    if flightplan.class_command == 1 and flightplan.id_command != 4:
                        if min_x <= fleet.x <= max_x and min_y <= fleet.y <= max_y and min_z <= fleet.z <= max_z:
                            system_x = int(fleet.x)
                            system_y = int(fleet.y)
                            system_z = int(fleet.z)
                            line = u'    №%s. %s : %s : %s  \n' % (fleet.id, system_x, system_y, system_z)
                            fleet_mail += line

                    elif flightplan.class_command != 1:
                        if min_x <= fleet.x <= max_x and min_y <= fleet.y <= max_y and min_z <= fleet.z <= max_z:
                            system_x = fleet.x
                            system_y = fleet.y
                            system_z = fleet.z
                            line = u'    №%s. %s : %s : %s  \n' % (fleet.id, system_x, system_y, system_z)
                            fleet_mail += line
                    final_mail = fleet_mail

            elif flightplan_scan.id_command == 4:
                flightplans = Flightplan.objects.filter(status=1, class_command=1, id_commant=4)
                for flightplan in flightplans:
                    fleet = Fleet.objects.filter(id=flightplan.fleet).first()
                    verification_flight(fleet)
                    mail_subject = u'Сканирование гиперпространства \n'
                    fleet_mail = u'Флот произвел сканирование, находясь на координатам %s : %s : %s.\n  ' \
                                 u'Координаты найденых в гипере флотов: \n' % (fleet_x, fleet_y, fleet_z)
                    if min_x <= fleet.x <= max_x and min_y <= fleet.y <= max_y and min_z <= fleet.z <= max_z:
                        system_x = fleet.x
                        system_y = fleet.y
                        system_z = fleet.z
                        line = u'    №%s. %s : %s : %s  \n' % (fleet.id, system_x, system_y, system_z)
                        fleet_mail += line
                    final_mail = fleet_mail

            mail = Mail(
                user=user,
                recipient=0,
                time=timezone.now(),
                status=1,
                category=4,
                login_recipient='Система',
                title=mail_subject,
                message=final_mail
            )
            mail.save()

            ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet.id)
            need_fuel = need_fuel_process(ship_in_fleets, flightplan, delta, fleet.id)
            minus_fuel(fleet, need_fuel)

            FlightplanScan.objects.filter(id_fleetplan=flightplan.id).delete()
            Flightplan.objects.filter(id=flightplan.id).delete()

            return finish_time
