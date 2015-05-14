# -*- coding: utf-8 -*-

from django.utils import timezone
from datetime import timedelta
import math
from my_game.models import Planet
from my_game.models import System, Asteroid_field, Flightplan_scan
from my_game.models import Fleet, Fuel_pattern, Fuel_tank
from my_game.models import Flightplan, Fleet_parametr_scan
from my_game.models import Mail
from my_game.flightplan.veryfication.flight_verification import verification_flight
from my_game.flightplan import fuel


def scan_veryfication(*args):
    fleet = args[0]
    user = fleet.user
    flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first()

    mail_subject = ''
    final_mail = ''
    flightplan_scan = Flightplan_scan.objects.filter(id_fleetplan=flightplan.id).first()
    finish_time = timezone.now()
    time = timezone.now()
    time_start = flightplan_scan.start_time
    delta_time = time - time_start
    new_delta = delta_time.seconds
    delta = flightplan_scan.time_scanning
    if new_delta > delta:
        finish_time = time_start + timedelta(seconds=delta)
        fleet_parametr_scan = Fleet_parametr_scan.objects.filter(fleet_id=fleet.id,
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
            mail_text = u'Флот произвел сканирование пространства, находясь на координатам %s : %s : %s. \n Координаты систем: \n' % (
                fleet_x, fleet_y, fleet_z)
            message_planet_subject = u''
            message_planet = u''
            for system in systems:
                if min_x <= system.x <= max_x and min_y <= system.y <= max_y and min_z <= system.z <= max_z:
                    system_x = int(system.x)
                    system_y = int(system.y)
                    system_z = int(system.z)
                    distance = int(
                        math.sqrt((fleet_x - system_x) ** 2 + (fleet_y - system_y) ** 2 + (fleet_z - system_z) ** 2))
                    if distance <= delta and distance != 0:
                        line = u' %s : %s : %s - растояние: %s св. \n' % (
                            system_x, system_y, system_z, int(distance / 1000))
                        if distance <= delta * 0.1:
                            message_planet_subject = u'  В системе найдены планеты с координатами: \n'
                            planets = Planet.objects.filter(system_id=system.id).order_by('planet_num')
                            for planet in planets:
                                mess_planet = u'    %s - %s : %s : %s \n' % (
                                planet.planet_num, planet.global_x, planet.global_y, planet.global_z)
                                message_planet = message_planet + mess_planet
                            line = line + message_planet_subject + message_planet
                        mail_text = mail_text + line
            final_mail = mail_text


        elif flightplan.id_command == 2:
            asteroid_fields = Asteroid_field.objects.all()
            size = 0
            mail_subject = u'Поиск астероидных полей \n'
            ast_mail = u'Флот произвел поиск астероидов, находясь на координатам %s : %s : %s.\n Координаты астероидных полей: \n' % (
            fleet_x, fleet_y, fleet_z)
            for asteroid_field in asteroid_fields:
                if min_x <= asteroid_field.x <= max_x and min_y <= asteroid_field.y <= max_y and min_z <= asteroid_field.z <= max_z:
                    system_x = int(asteroid_field.x)
                    system_y = int(asteroid_field.y)
                    system_z = int(asteroid_field.z)
                    asteroid_size = asteroid_field.size
                    size = size + asteroid_field.size
                    distance = int(
                        math.sqrt((fleet_x - system_x) ** 2 + (fleet_y - system_y) ** 2 + (fleet_z - system_z) ** 2))
                    if distance <= delta:
                        line = u'%s : %s : %s  Размер:%s Растояние:%s св. \n ' % (
                            system_x, system_y, system_z, asteroid_size, int(distance / 1000))
                        ast_mail = ast_mail + line
            size = u'Общий размер найденных полей: %s' % (size)
            final_mail = ast_mail + size

        elif flightplan_scan.id_command == 3:
            fleets = Fleet.objects.filter(status=1)

            for fleet in fleets:
                verification_flight(fleet)
            fleets = Fleet.objects.all()
            mail_subject = u'Сканирование пространства \n'
            fleet_mail = u'Флот произвел сканирование, находясь на координатам %s : %s : %s.\n Координаты найденых флотов: \n' % (
            fleet_x, fleet_y, fleet_z)
            for fleet in fleets:
                flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first()
                if flightplan.class_command == 1 and flightplan.id_command != 4:
                    if min_x <= fleet.x <= max_x and min_y <= fleet.y <= max_y and min_z <= fleet.z <= max_z:
                        system_x = int(fleet.x)
                        system_y = int(fleet.y)
                        system_z = int(fleet.z)
                        line = u'%s : %s : %s  \n' % (system_x, system_y, system_z)
                        fleet_mail = fleet_mail + line

                elif flightplan.class_command != 1:
                    if min_x <= fleet.x <= max_x and min_y <= fleet.y <= max_y and min_z <= fleet.z <= max_z:
                        system_x = fleet.x
                        system_y = fleet.y
                        system_z = fleet.z
                        line = u'%s : %s : %s \n' % (system_x, system_y, system_z)
                        fleet_mail = fleet_mail + line
                final_mail = fleet_mail

        elif flightplan_scan.id_command == 4:
            flightplans = Flightplan.objects.filter(status=1, class_command=1, id_commant=4)
            for flightplan in flightplans:
                fleet = Fleet.objects.filter(id=flightplan.id_fleet).first()
                verification_flight(fleet)
                mail_subject = u'Сканирование гиперпространства \n'
                fleet_mail = u'Флот произвел сканирование, находясь на координатам %s : %s : %s.\n Координаты найденых в гипере флотов: \n' % (
                fleet_x, fleet_y, fleet_z)
                if min_x <= fleet.x <= max_x and min_y <= fleet.y <= max_y and min_z <= fleet.z <= max_z:
                    system_x = fleet.x
                    system_y = fleet.y
                    system_z = fleet.z
                    line = u'%s : %s : %s \n' % (system_x, system_y, system_z)
                    fleet_mail = fleet_mail + line
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
        fuel_tank = Fuel_tank.objects.filter(fleet_id=fleet.id).first()
        fuel_pattern = Fuel_pattern.objects.filter(user=fleet.user, fuel_class=fuel_tank.fuel_class).first()

        need_fuel = fuel.fuel_scan(fleet.id, flightplan_scan, flightplan)
        need_fuel = need_fuel / fuel_pattern.efficiency

        new_fuel = int(fuel_tank.amount_fuel - need_fuel)
        new_mass = int(fuel_tank.mass_fuel - need_fuel * fuel_pattern.mass)
        new_size = int(fuel_tank.size_fuel - need_fuel * fuel_pattern.size)
        fuel_tank = Fuel_tank.objects.filter(id=fuel_tank.id, fleet_id=fleet.id).update(amount_fuel=new_fuel,
                                                                                        mass_fuel=new_mass,
                                                                                        size_fuel=new_size)
        flightplan_scan = Flightplan_scan.objects.filter(id_fleetplan=flightplan.id).delete()
        flightplan = Flightplan.objects.filter(id=flightplan.id).delete()

        return finish_time

