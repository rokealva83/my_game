# -*- coding: utf-8 -*-

from my_game.models import FactoryPattern, HullPattern, ArmorPattern, ShellPattern, ShieldPattern, \
    GeneratorPattern, WeaponPattern, EnginePattern, ModulePattern, DevicePattern, FuelPattern
from space_forces.hold_and_tank.unloading import unloading
from space_forces.hold_and_tank.unload_hold_resources import unload_hold_resources


def unload_hold(*args):
    session_user = args[0]
    session_user_city = args[1]
    fleet = args[2]
    my_dictionary = args[3]

    amount_factory = my_dictionary.get('amount_factory')
    if amount_factory is not None:
        shipment_id_fac = my_dictionary.get('hidden_factory')
        len_factory_amount = len(amount_factory)
        for i in range(len_factory_amount):
            factory_amount = int(amount_factory[i])
            if factory_amount != 0:
                shipment_id = int(shipment_id_fac[i])
                class_shipment = 10
                factory = FactoryPattern.objects.filter(id=shipment_id).first()
                size = int(factory.factory_size) * factory_amount
                amount_shipment = factory_amount
                mass_shipment = int(factory.factory_mass) * factory_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_hull = my_dictionary.get('amount_hull')
    if amount_hull is not None:
        shipment_id_hull = my_dictionary.get('hidden_hull')
        len_hull_amount = len(amount_hull)
        for i in range(len_hull_amount):
            hull_amount = int(amount_hull[i])
            if hull_amount != 0:
                shipment_id = int(shipment_id_hull[i])
                class_shipment = 1
                hull = HullPattern.objects.filter(id=shipment_id).first()
                size = int(hull.hull_size) * hull_amount
                amount_shipment = hull_amount
                mass_shipment = int(hull.hull_mass) * hull_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_armor = my_dictionary.get('amount_armor')
    if amount_armor is not None:
        shipment_id_arm = my_dictionary.get('hidden_armor')
        len_armor_amount = len(amount_armor)
        for i in range(len_armor_amount):
            armor_amount = int(amount_armor[0])
            if armor_amount != 0:
                shipment_id = int(shipment_id_arm[i])
                class_shipment = 2
                armor = ArmorPattern.objects.filter(id=shipment_id).first()
                size = 15 * armor_amount
                amount_shipment = armor_amount
                mass_shipment = int(armor.armor_mass) * armor_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_shield = my_dictionary.get('amount_shield')
    if amount_shield is not None:
        shipment_id_shield = my_dictionary.get('hidden_shield')
        len_shield_amount = len(amount_shield)
        for i in range(len_shield_amount):
            shield_amount = int(amount_shield[i])
            if shield_amount != 0:
                shipment_id = int(shipment_id_shield[i])
                class_shipment = 3
                shield = ShieldPattern.objects.filter(id=shipment_id).first()
                size = int(shield.shield_size) * shield_amount
                amount_shipment = shield_amount
                mass_shipment = int(shield.shield_mass) * shield_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_engine = my_dictionary.get('amount_engine')
    if amount_engine is not None:
        shipment_id_eng = my_dictionary.get('hidden_engine')
        len_engine_amount = len(amount_engine)
        for i in range(len_engine_amount):
            engine_amount = int(amount_engine[i])
            if engine_amount != 0:
                shipment_id = int(shipment_id_eng[i])
                class_shipment = 4
                engine = EnginePattern.objects.filter(id=shipment_id).first()
                size = int(engine.engine_size) * engine_amount
                amount_shipment = engine_amount
                mass_shipment = int(engine.engine_mass) * engine_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_generator = my_dictionary.get('amount_generator')
    if amount_generator is not None:
        shipment_id_gen = my_dictionary.get('hidden_generator')
        len_generator_amount = len(amount_generator)
        for i in range(len_generator_amount):
            generator_amount = int(amount_generator[i])
            if generator_amount != 0:
                shipment_id = int(shipment_id_gen[i])
                class_shipment = 5
                generator = GeneratorPattern.objects.filter(id=shipment_id).first()
                size = int(generator.generator_size) * generator_amount
                amount_shipment = generator_amount
                mass_shipment = int(generator.generator_mass) * generator_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_weapon = my_dictionary.get('amount_weapon')
    if amount_weapon is not None:
        shipment_id_weap = my_dictionary.get('hidden_weapon')
        len_weapon_amount = len(amount_weapon)
        for i in range(len_weapon_amount):
            weapon_amount = int(amount_weapon[i])
            if weapon_amount != 0:
                shipment_id = int(shipment_id_weap[i])
                class_shipment = 6
                weapon = WeaponPattern.objects.filter(id=shipment_id).first()
                size = int(weapon.weapon_size) * weapon_amount
                amount_shipment = weapon_amount
                mass_shipment = int(weapon.weapon_mass) * weapon_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_shell = my_dictionary.get('amount_shell')
    if amount_shell is not None:
        shipment_id_shell = my_dictionary.get('hidden_shell')
        len_shell_amount = len(amount_shell)
        for i in range(len_shell_amount):
            shell_amount = int(amount_shell[i])
            if shell_amount != 0:
                shipment_id = int(shipment_id_shell[i])
                class_shipment = 7
                shell = ShellPattern.objects.filter(id=shipment_id).first()
                size = int(shell.shell_size) * shell_amount
                amount_shipment = shell_amount
                mass_shipment = int(shell.shell_mass) * shell_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_module = my_dictionary.get('amount_module')
    if amount_module is not None:
        shipment_id_mod = my_dictionary.get('hidden_module')
        len_module_amount = len(amount_module)
        for i in range(len_module_amount):
            module_amount = int(amount_module[i])
            if module_amount != 0:
                shipment_id = int(shipment_id_mod[i])
                class_shipment = 8
                module = ModulePattern.objects.filter(id=shipment_id).first()
                size = int(module.module_size) * module_amount
                amount_shipment = module_amount
                mass_shipment = int(module.module_mass) * module_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_device = my_dictionary.get('amount_device')
    if amount_device is not None:
        shipment_id_device = my_dictionary.get('hidden_device')
        len_device_amount = len(amount_device)
        for i in range(len_device_amount):
            device_amount = int(amount_device[i])
            if device_amount != 0:
                shipment_id = int(shipment_id_device[i])
                class_shipment = 9
                device = DevicePattern.objects.filter(id=shipment_id).first()
                size = int(device.device_size) * device_amount
                amount_shipment = device_amount
                mass_shipment = int(device.device_mass) * device_amount
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

    amount_fuel = my_dictionary.get('amount_fuel')
    if amount_fuel is not None:
        shipment_id_fuel = my_dictionary.get('hidden_fuel')
        len_fuel_amount = len(amount_fuel)
        for i in range(len_fuel_amount):
            amount_fuel = int(amount_fuel[i])
            if amount_fuel != 0:
                shipment_id = int(shipment_id_fuel[i])
                class_shipment = 14
                fuel = FuelPattern.objects.filter(id=shipment_id).first()
                size = int(fuel.fuel_size) * amount_fuel
                amount_shipment = amount_fuel
                mass_shipment = int(fuel.fuel_mass) * amount_fuel
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)
    unload_hold_resources(session_user, session_user_city, fleet, my_dictionary)
    message = 'Ресурсы выгружено'
    return message
