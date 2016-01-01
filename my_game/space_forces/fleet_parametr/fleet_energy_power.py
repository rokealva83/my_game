# -*- coding: utf-8 -*-

from my_game.models import ModulePattern, EnginePattern, GeneratorPattern, ShieldPattern, WeaponPattern


def fleet_energy_power(*args):
    fleet = args[0]
    ship = args[1]
    ship_elements = args[2]
    amount_ship = args[3]
    use_energy = ship.project_ship.hull_pattern.power_consuption
    use_fuel_system = use_fuel_intersystem = use_energy_giper = 0
    use_energy_null = use_fuel_generator = produced_energy = 0
    for ship_element in ship_elements:
        if ship_element.class_element == 3:
            element_pattern = ShieldPattern.objects.filter(
                id=ship_element.element_pattern_id).first()
            use_energy += element_pattern.power_consuption

        if ship_element.class_element == 4:
            engine_pattern = EnginePattern.objects.filter(
                id=ship_element.element_pattern_id).first()
            if engine_pattern.system_power != 0:
                use_fuel_system += engine_pattern.power_consuption
            if engine_pattern.intersystem_power != 0:
                use_fuel_intersystem += engine_pattern.power_consuption
            if engine_pattern.giper_power != 0:
                use_energy_giper = use_energy_giper + engine_pattern.power_consuption
            if engine_pattern.nullT_power != 0:
                use_energy_null += engine_pattern.power_consuption

        if ship_element.class_element == 5:
            element_pattern = GeneratorPattern.objects.filter(
                id=ship_element.element_pattern_id).first()
            use_fuel_generator = use_fuel_generator + element_pattern.fuel_necessary
            produced_energy = produced_energy + element_pattern.produced_energy

        if ship_element.class_element == 6:
            element_pattern = WeaponPattern.objects.filter(
                id=ship_element.element_pattern_id).first()
            use_energy = use_energy + element_pattern.power_consuption

        if ship_element.class_element == 7:
            element_pattern = WeaponPattern.objects.filter(
                id=ship_element.element_pattern_id).first()
            use_energy = use_energy + element_pattern.power_consuption

        if ship_element.class_element == 8:
            element_pattern = ModulePattern.objects.filter(
                id=ship_element.element_pattern_id).first()
            use_energy = use_energy + element_pattern.power_consuption

    fleet_energy = fleet.fleet_energy_power
    new_use_energy = fleet_energy.use_energy + use_energy * amount_ship * args[4]
    new_use_fuel_system = fleet_energy.use_fuel_system + use_fuel_system * amount_ship * args[4]
    new_use_fuel_intersystem = fleet_energy.use_fuel_intersystem + use_fuel_intersystem * amount_ship * args[4]
    new_use_energy_giper = fleet_energy.use_energy_giper + use_energy_giper * amount_ship * args[4]
    new_use_energy_null = fleet_energy.use_energy_null + use_energy_null * amount_ship * args[4]
    new_produce_energy = fleet_energy.produce_energy + produced_energy * amount_ship * args[4]
    new_use_fuel_generator = fleet_energy.use_fuel_generator + use_fuel_generator * amount_ship * args[4]

    setattr(fleet_energy, 'use_energy', new_use_energy)
    setattr(fleet_energy, 'use_fuel_system', new_use_fuel_system)
    setattr(fleet_energy, 'use_fuel_intersystem', new_use_fuel_intersystem)
    setattr(fleet_energy, 'use_energy_giper', new_use_energy_giper)
    setattr(fleet_energy, 'use_energy_null', new_use_energy_null)
    setattr(fleet_energy, 'produce_energy', new_produce_energy)
    setattr(fleet_energy, 'use_fuel_generator', new_use_fuel_generator)
    fleet_energy.save()

    return True
