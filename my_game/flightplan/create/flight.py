# -*- coding: utf-8 -*-

import math
from my_game.models import System, Planet
from my_game.models import Fleet
from my_game.models import Flightplan, FlightplanFlight
from my_game.flightplan.create.calculation import calculation


def flight_system(*args):
    session_user = args[0]
    fleet = args[2]
    request = args[3]
    fleet_engine = Fleet.fleet_engine
    city = request.POST.get('city')
    coordinate = request.POST.get('coordinate')
    message = ''
    if city:
        planet_system = int(request.POST.get('planet_system'))
        planet_planet = int(request.POST.get('planet_planet'))
        planet_giper = request.POST.get('planet_giper')
        planet_null = request.POST.get('planet_null')
        target_system = System.objects.filter(id=planet_system).first()
        target_planet = Planet.objects.filter(system=target_system, planet_num=planet_planet).first()
        if target_planet:
            system = System.objects.filter(id=fleet.system_id).first()
            flightplan_flight = FlightplanFlight.objects.filter(fleet=fleet).last()
            if flightplan_flight:
                xx1 = flightplan_flight.finish_x
                yy1 = flightplan_flight.finish_y
                zz1 = flightplan_flight.finish_z

            else:
                xx1 = int(fleet.x)
                yy1 = int(fleet.y)
                zz1 = int(fleet.z)

            if target_planet:
                xx2 = int(target_planet.global_x)
                yy2 = int(target_planet.global_y)
                zz2 = int(target_planet.global_z)

            else:
                distance = math.sqrt((xx1 - int(target_system.x)) ** 2 + (yy1 - int(target_system.y)) ** 2 + (
                    zz1 - int(target_system.z)) ** 2)
                xx2 = xx1 + (int(target_system.x) - xx1) * (distance - int(target_system.system_size)) / distance
                yy2 = yy1 + (int(target_system.y) - yy1) * (distance - int(target_system.system_size)) / distance
                zz2 = zz1 + (int(target_system.z) - zz1) * (distance - int(target_system.system_size)) / distance

            distance = math.sqrt((xx1 - xx2) ** 2 + (yy1 - yy2) ** 2 + (zz1 - zz2) ** 2)

            if fleet.system_id != 0:
                system = System.objects.filter(id=fleet.system_id).first()
            else:
                flightplan_flight = FlightplanFlight.objects.filter(fleet=fleet).last()
                if flightplan_flight:
                    system = System.objects.filter(id=flightplan_flight.system_id).first()

            if system:
                if int(system.id) == planet_system:
                    flight_time = math.sqrt(
                        distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet_engine.system_power)) * 2
                    command_id = 1
                else:
                    answer = calculation(fleet, planet_giper, planet_null, distance)
                    command_id = answer['command_id']
                    flight_time = answer['flight_time']
            else:
                answer = calculation(fleet, planet_giper, planet_null, distance)
                command_id = answer['command_id']
                flight_time = answer['flight_time']

            if command_id != 1:
                system_flight = 0
            else:
                system_flight = 1

            flightplan = Flightplan(
                user=session_user,
                fleet=fleet,
                class_command=1,
                command_id=command_id,
                status=0,
            )
            flightplan.save()
            flightplan_flight = FlightplanFlight(
                user=session_user,
                fleet=fleet,
                flightplan=flightplan,
                command_id=command_id,
                start_x=xx1,
                start_y=yy1,
                start_z=zz1,
                finish_x=int(xx2),
                finish_y=int(yy2),
                finish_z=int(zz2),
                flight_time=flight_time,
                planet_id=planet_planet,
                system_id=planet_system,
                system_flight=system_flight
            )
            flightplan_flight.save()
        else:
            message = 'Планеты не существует'

    if coordinate:
        coordinate_x = float(request.POST.get('coordinate_x'))
        coordinate_y = float(request.POST.get('coordinate_y'))
        coordinate_z = float(request.POST.get('coordinate_z'))
        coordinate_giper = request.POST.get('coordinate_giper')
        coordinate_null = request.POST.get('coordinate_null')
        flightplan_flight = FlightplanFlight.objects.filter(fleet=fleet).last()

        if flightplan_flight:
            xx1 = flightplan_flight.finish_x
            yy1 = flightplan_flight.finish_y
            zz1 = flightplan_flight.finish_z
        else:
            xx1 = int(fleet.x)
            yy1 = int(fleet.y)
            zz1 = int(fleet.z)

        xx2 = coordinate_x
        yy2 = coordinate_y
        zz2 = coordinate_z
        distance = math.sqrt((xx1 - xx2) ** 2 + (yy1 - yy2) ** 2 + (zz1 - zz2) ** 2)

        answer = calculation(fleet, coordinate_giper, coordinate_null, distance)
        command_id = answer['command_id']
        flight_time = answer['flight_time']

        system = 0
        planet = Planet.objects.filter(global_x=coordinate_x, global_y=coordinate_y, global_z=coordinate_z).first()
        if planet:
            planet = planet.planet_num
            system = planet.system_id
        else:
            planet = 0

        if command_id != 1:
            system_flight = 0
        else:
            system_flight = 1

        flightplan = Flightplan(
            user=session_user,
            fleet=fleet,
            class_command=1,
            command_id=command_id,
            status=0,
        )
        flightplan.save()

        flightplan = flightplan.pk
        flightplan_flight = FlightplanFlight(
            user=session_user,
            fleet=fleet,
            flightplan=flightplan,
            command_id=command_id,
            start_x=xx1,
            start_y=yy1,
            start_z=zz1,
            finish_x=xx2,
            finish_y=yy2,
            finish_z=zz2,
            flight_time=flight_time,
            planet_id=planet,
            system_id=system,
            system_flight=system_flight
        )
        flightplan_flight.save()

    return message
