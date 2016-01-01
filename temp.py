# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import ElementShip, ModulePattern, EnginePattern, GeneratorPattern, ShieldPattern, WeaponPattern
from my_game.models import ProjectShip, Ship, Fleet, FleetParametrScan, FleetEngine, FleetEnergyPower, FleetParametrResourceExtraction, FleetParametrBuildRepair
from my_game import function
from my_game.space_forces.ship_output import ship_output


def add_ship(request):
	if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        flightplans = flightplan_flights = warehouse_factorys = {}
        command = 1
        hold = ship_id = amount_ship = 0
        message = ''
        fleet_id = 0
        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())
        amount_ship_dict = my_dictionary.get('amount_ship')
        fleet_id_dict = my_dictionary.get('hidden_fleet')
        ship_id_dict = my_dictionary.get('hidden_ship')
        len_amount_ship_dict = int(len(amount_ship_dict))
        for i in range(len_amount_ship_dict):
            if int(amount_ship_dict[i]) != 0:
                amount_ship = int(amount_ship_dict[i])
                fleet_id = int(fleet_id_dict[i])
                ship_id = int(ship_id_dict[i])
        if amount_ship and fleet_id and ship_id:
        	ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0, place_id=session_user_city.id).first()
            fleet = Fleet.objects.filter(id=fleet_id).first()
            fleet_engine = FleetEngine.objects.filter(fleet=fleet).first()
            fleet_energy_power = FleetEnergyPower.objects.filter(fleet=fleet).first()
            city_planet = int(session_user_city.planet.id)
            fleet_planet = int(fleet.planet_id)
            if fleet.status == 0 and city_planet == fleet_planet:
            	added_ship_fleet = Ship.objects.filter(project_ship=ship.project_ship, user=session_user, fleet_status=1, place_id=fleet.id).first()
                other_ship_in_fleet = Ship.objects.filter(user=session_user, fleet_status=1, place_id=fleet.id).first()

                if amount_ship == ship.amount_ship:
                	if added_ship_fleet:
                		new_amount = ship.amount_ship + amount_ship
                		setattr(added_ship_fleet, 'amount_ship', new_amount)
                		added_ship_fleet.save()
	                	Ship.objects.filter(id=ship.id).delete()
	                else:
	                	setattr(ship, 'fleet_status', 1)
	                	setattr(ship, 'place_id', fleet_id)
                		ship.save()
                else:
                	new_planet_amount = ship.amount_ship - amount_ship
                	setattr(ship, 'amount_ship', new_planet_amount)
                	ship.save()
                	if added_ship_fleet:
                		new_fleet_amount = added_ship_fleet.amount_ship + amount_ship
                		setattr(added_ship_fleet, 'amount_ship', new_fleet_amount)
                		added_ship_fleet.save()
	                else:
	                	new_fleet_ship = Ship(
	                		user=session_user,
	                		project_ship=ship.project_ship,
	                		ship_name=ship.ship_name,
	                		amount_ship=amount_ship,
	                		fleet_status=1,
	                		place_id=fleet_id
	                		)
	                	new_fleet_ship.save()

	            fleet = fleet_parametr(fleet_id, ship, amount_ship)

def fleet_parametr(*args):
	fleet_id = args[0]
	ship = args[1]
	amount_ship = args[2]
	fleet = Fleet.objects.filter(id=fleet_id).first()
	empty_hold = fleet.empty_hold + ship.project_ship.hull_pattern.hold_size * amount_ship
	ship_empty_mass = fleet.ship_empty_mass + ship.project_ship.ship_mass * amount_ship
    free_fuel_tank = fleet.free_fuel_tank + ship.project_ship.hull_pattern.fuel_tank * amount_ship
    setattr(fleet, 'empty_hold', empty_hold)
    setattr(fleet, 'ship_empty_mass', ship_empty_mass)
    setattr(fleet, 'free_fuel_tank', free_fuel_tank)
    fleet.save()
    ship_elements = ElementShip.objects.filter(project_ship=ship.project_ship).all()
    fleet()
    return fleet

def fleet_engine_parametr(*args):
	

def fleet_scan_parametr(*args):

def fleet_energy_power(*args):
