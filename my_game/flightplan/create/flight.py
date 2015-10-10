# -*- coding: utf-8 -*-

import math
from my_game.models import System, Planet
from my_game.models import ProjectShip, Ship, Fleet, FleetEngine
from my_game.models import Flightplan, FlightplanFlight


def flight_system(*args):
    session_user = args[0]
    request = args[2]
    fleet_id = int(request.POST.get('hidden_fleet'))
    fleet_engine = FleetEngine.objects.filter(fleet_id=fleet_id).first()
    fleet = Fleet.objects.filter(id=fleet_id).first()
    city = request.POST.get('city')
    coordinate = request.POST.get('coordinate')
    message = ''
    if city:
        planet_system = int(request.POST.get('planet_system'))
        planet_planet = int(request.POST.get('planet_planet'))
        planet_giper = request.POST.get('planet_giper')
        planet_null = request.POST.get('planet_null')
        target_system = System.objects.filter(id=planet_system).first()
        target_planet = Planet.objects.filter(system_id=planet_system, planet_num=planet_planet).first()
        if target_planet:
            system = System.objects.filter(id=fleet.system).first()

            flightplan_flight = FlightplanFlight.objects.filter(id_fleet=fleet_id).last()

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

            if fleet.system != 0:
                system = System.objects.filter(id=fleet.system).first()
            else:
                flightplan_flight = FlightplanFlight.objects.filter(id_fleet=fleet_id).last()
                if flightplan_flight:
                    system = flightplan_flight.system

            if system:
                if int(system.id) == planet_system:
                    flight_time = math.sqrt(
                        distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet_engine.system_power)) * 2
                    id_command = 1
                else:
                    answer = calculation(fleet_id, planet_giper, planet_null, distance)
                    id_command = answer['command_id']
                    flight_time = answer['flight_time']
            else:
                answer = calculation(fleet_id, planet_giper, planet_null, distance)
                id_command = answer['command_id']
                flight_time = answer['flight_time']

            if id_command != 1:
                system_flight = 0
            else:
                system_flight = 1

            flightplan = Flightplan(
                user=session_user,
                id_fleet=fleet_id,
                class_command=1,
                id_command=id_command,
                status=0,
            )
            flightplan.save()
            id_fleetplan = flightplan.pk
            flightplan_flight = FlightplanFlight(
                user=session_user,
                id_fleet=fleet_id,
                id_fleetplan=id_fleetplan,
                id_command=id_command,
                start_x=xx1,
                start_y=yy1,
                start_z=zz1,
                finish_x=int(xx2),
                finish_y=int(yy2),
                finish_z=int(zz2),
                flight_time=flight_time,
                planet=planet_planet,
                system=planet_system,
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
        fleet = Fleet.objects.filter(id=fleet_id).first()
        flightplan_flight = FlightplanFlight.objects.filter(id_fleet=fleet_id).last()

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

        answer = calculation(fleet_id, coordinate_giper, coordinate_null, distance)
        id_command = answer['command_id']
        flight_time = answer['flight_time']

        system = 0
        planet = Planet.objects.filter(global_x=coordinate_x, global_y=coordinate_y, global_z=coordinate_z).first()
        if planet:
            planet = planet.planet_num
            system = planet.system_id
        else:
            planet = 0

        if id_command != 1:
            system_flight = 0
        else:
            system_flight = 1

        flightplan = Flightplan(
            user=session_user,
            id_fleet=fleet_id,
            class_command=1,
            id_command=id_command,
            status=0,
        )
        flightplan.save()

        id_fleetplan = flightplan.pk
        flightplan_flight = FlightplanFlight(
            user=session_user,
            id_fleet=fleet_id,
            id_fleetplan=id_fleetplan,
            id_command=id_command,
            start_x=xx1,
            start_y=yy1,
            start_z=zz1,
            finish_x=xx2,
            finish_y=yy2,
            finish_z=zz2,
            flight_time=flight_time,
            planet=planet,
            system=system,
            system_flight=system_flight
        )
        flightplan_flight.save()

    return message


def calculation(*args):
    fleet_id = args[0]
    coordinate_giper = args[1]
    coordinate_null = args[2]
    distance = args[3]
    fleet = Fleet.objects.filter(id=fleet_id).first()
    fleet_engine = FleetEngine.objects.filter(fleet_id=fleet_id).first()
    if coordinate_giper:
        fleet_ships = Ship.objects.filter(place_id=fleet_id, fleet_status=1)
        check = 0
        for fleet_ship in fleet_ships:
            project_ship = ProjectShip.objects.filter(id=fleet_ship.project_ship).first()
            if project_ship.giper_power == 0:
                check = 1
        if check == 0:
            flight_time = math.sqrt(
                distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet_engine.giper_power)) * 2
            id_command = 3
        else:
            flight_time = math.sqrt(
                distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet_engine.intersystem_power)) * 2
            id_command = 2
    elif coordinate_null:
        fleet_ships = Ship.objects.filter(place_id=fleet_id, fleet_status=1)
        check = 0
        for fleet_ship in fleet_ships:
            project_ship = ProjectShip.objects.filter(id=fleet_ship.project_ship).first()
            if project_ship.giper_power == 0:
                check = 1
        if check == 0:
            flight_time = math.sqrt(
                distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet_engine.null_power)) * 2
            id_command = 4
        else:
            flight_time = math.sqrt(
                distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet_engine.intersystem_power)) * 2
            id_command = 2
    else:
        flight_time = math.sqrt(
            distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet_engine.intersystem_power)) * 2
        id_command = 2
    return {'flight_time': flight_time, 'command_id': id_command}
