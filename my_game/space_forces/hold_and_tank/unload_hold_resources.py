# -*- coding: utf-8 -*-

from my_game.models import Fleet


def unload_hold_resources(*args):
    session_user_city = args[1]
    fleet = args[2]
    my_dictionary = args[3]
    mass = size = 0
    resource_hold = fleet.resource_hold
    warehouse = session_user_city.warehouse
    if my_dictionary.get('res_nickel'):
        amount = int(my_dictionary.get('res_nickel')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.res_nickel
        if amount != 0:
            if resource_hold.res_nickel < amount:
                amount = resource_hold.res_nickel
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.res_nickel + amount
            new_amount_fleet = resource_hold.res_nickel - amount
            setattr(resource_hold, 'res_nickel', new_amount_fleet)
            setattr(warehouse, 'res_nickel', new_amount_warehouse)

    if my_dictionary.get('res_iron'):
        amount = int(my_dictionary.get('res_iron')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.res_iron
        if amount != 0:
            if resource_hold.res_iron < amount:
                amount = resource_hold.res_iron
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.res_iron + amount
            new_amount_fleet = resource_hold.res_iron - amount
            setattr(resource_hold, 'res_iron', new_amount_fleet)
            setattr(warehouse, 'res_iron', new_amount_warehouse)

    if my_dictionary.get('res_aluminum'):
        amount = int(my_dictionary.get('res_aluminum')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.res_aluminum
        if amount != 0:
            if resource_hold.res_aluminum < amount:
                amount = resource_hold.res_aluminum
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.res_aluminum + amount
            new_amount_fleet = resource_hold.res_aluminum - amount
            setattr(resource_hold, 'res_aluminum', new_amount_fleet)
            setattr(warehouse, 'res_aluminum', new_amount_warehouse)

    if my_dictionary.get('res_cooper'):
        amount = int(my_dictionary.get('res_cooper')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.res_cooper
        if amount != 0:
            if resource_hold.res_cooper < amount:
                amount = resource_hold.res_cooper
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.res_cooper + amount
            new_amount_fleet = resource_hold.res_cooper - amount
            setattr(resource_hold, 'res_cooper', new_amount_fleet)
            setattr(warehouse, 'res_cooper', new_amount_warehouse)

    if my_dictionary.get('res_veriarit'):
        amount = int(my_dictionary.get('res_veriarit')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.res_veriarit
        if amount != 0:
            if resource_hold.res_veriarit < amount:
                amount = resource_hold.res_veriarit
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.res_veriarit + amount
            new_amount_fleet = resource_hold.res_veriarit - amount
            setattr(resource_hold, 'res_veriarit', new_amount_fleet)
            setattr(warehouse, 'res_veriarit', new_amount_warehouse)

    if my_dictionary.get('res_inneilit'):
        amount = int(my_dictionary.get('res_inneilit')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.res_inneilit
        if amount != 0:
            if resource_hold.res_inneilit < amount:
                amount = resource_hold.res_inneilit
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.res_inneilit + amount
            new_amount_fleet = resource_hold.res_inneilit - amount
            setattr(resource_hold, 'res_inneilit', new_amount_fleet)
            setattr(warehouse, 'res_inneilit', new_amount_warehouse)

    if my_dictionary.get('res_renniit'):
        amount = my_dictionary.get('res_renniit')[0]
        if my_dictionary.get('unload_all'):
            amount = resource_hold.res_renniit
        if amount != 0:
            if resource_hold.res_renniit < amount:
                amount = resource_hold.res_renniit
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.res_renniit + amount
            new_amount_fleet = resource_hold.res_renniit - amount
            setattr(resource_hold, 'res_renniit', new_amount_fleet)
            setattr(warehouse, 'res_renniit', new_amount_warehouse)

    if my_dictionary.get('res_cobalt'):
        amount = int(my_dictionary.get('res_cobalt')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.res_cobalt
        if amount != 0:
            if resource_hold.res_cobalt < amount:
                amount = resource_hold.res_cobalt
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.res_cobalt + amount
            new_amount_fleet = resource_hold.res_cobalt - amount
            setattr(resource_hold, 'res_cobalt', new_amount_fleet)
            setattr(warehouse, 'res_cobalt', new_amount_warehouse)

    if my_dictionary.get('mat_construction_material'):
        amount = int(my_dictionary.get('mat_construction_material')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.mat_construction_material
        if amount != 0:
            if resource_hold.res_cmat_construction_materialobalt < amount:
                amount = resource_hold.mat_construction_material
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.mat_construction_material + amount
            new_amount_fleet = resource_hold.mat_construction_material - amount
            setattr(resource_hold, 'mat_construction_material', new_amount_fleet)
            setattr(warehouse, 'mat_construction_material', new_amount_warehouse)

    if my_dictionary.get('mat_chemical'):
        amount = int(my_dictionary.get('mat_chemical')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.mat_chemical
        if amount != 0:
            if resource_hold.mat_chemical < amount:
                amount = resource_hold.mat_chemical
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.mat_chemical + amount
            new_amount_fleet = resource_hold.mat_chemical - amount
            setattr(resource_hold, 'mat_chemical', new_amount_fleet)
            setattr(warehouse, 'mat_chemical', new_amount_warehouse)

    elif my_dictionary.get('mat_high_strength_allov'):
        amount = int(my_dictionary.get('mat_high_strength_allov')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.mat_high_strength_allov
        if amount != 0:
            if resource_hold.mat_high_strength_allov < amount:
                amount = resource_hold.mat_high_strength_allov
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.mat_high_strength_allov + amount
            new_amount_fleet = resource_hold.mat_high_strength_allov - amount
            setattr(resource_hold, 'mat_high_strength_allov', new_amount_fleet)
            setattr(warehouse, 'mat_high_strength_allov', new_amount_warehouse)

    elif my_dictionary.get('mat_nanoelement'):
        amount = int(my_dictionary.get('mat_nanoelement')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.mat_nanoelement
        if amount != 0:
            if resource_hold.mat_nanoelement < amount:
                amount = resource_hold.mat_nanoelement
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.mat_nanoelement + amount
            new_amount_fleet = resource_hold.mat_nanoelement - amount
            setattr(resource_hold, 'mat_nanoelement', new_amount_fleet)
            setattr(warehouse, 'mat_nanoelement', new_amount_warehouse)

    elif my_dictionary.get('mat_microprocessor_element'):
        amount = int(my_dictionary.get('mat_microprocessor_element')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.mat_microprocessor_element
        if amount != 0:
            if resource_hold.mat_microprocessor_element < amount:
                amount = resource_hold.mat_microprocessor_element
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.mat_microprocessor_element + amount
            new_amount_fleet = resource_hold.mat_microprocessor_element - amount
            setattr(resource_hold, 'mat_microprocessor_element', new_amount_fleet)
            setattr(warehouse, 'mat_microprocessor_element', new_amount_warehouse)

    elif my_dictionary.get('mat_fober_optic_element'):
        amount = int(my_dictionary.get('mat_fober_optic_element')[0])
        if my_dictionary.get('unload_all'):
            amount = resource_hold.mat_fober_optic_element
        if amount != 0:
            if resource_hold.mat_fober_optic_element < amount:
                amount = resource_hold.mat_fober_optic_element
            mass += amount
            size += amount
            new_amount_warehouse = warehouse.mat_fober_optic_element + amount
            new_amount_fleet = resource_hold.mat_fober_optic_element - amount
            setattr(resource_hold, 'mat_fober_optic_element', new_amount_fleet)
            setattr(warehouse, 'mat_fober_optic_element', new_amount_warehouse)

    resource_hold.save()
    warehouse.save()

    new_fleet_mass = fleet.ship_empty_mass - mass
    new_empty_hold = fleet.empty_hold + size
    new_hold = fleet.fleet_hold - size
    Fleet.objects.filter(id=fleet.id).update(ship_empty_mass=new_fleet_mass, empty_hold=new_empty_hold,
                                             fleet_hold=new_hold)

    return True
