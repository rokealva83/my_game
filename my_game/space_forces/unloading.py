# -*- coding: utf-8 -*-

from my_game.models import Warehouse, WarehouseElement, WarehouseFactory
from my_game.models import Fleet, Hold


def unloading(*args):
    session_user = args[0]
    session_user_city = args[1]
    fleet = args[2]
    class_shipment = args[3]
    shipment_id = args[4]
    amount_shipment = args[5]

    hold = Hold.objects.filter(fleet=fleet, class_shipment=class_shipment, shipment_id=shipment_id).first()
    hold_amount_shipment = hold.amount_shipment

    if class_shipment == 0:
        # resource_attribures = ['res_nickel', 'res_iron', 'res_cooper', 'res_aluminum', 'res_veriarit', 'res_inneilit',
        #                       'res_renniit', 'res_cobalt', 'mat_construction_material', 'mat_chemical',
        #                       'mat_high_strength_allov', 'mat_nanoelement', 'mat_microprocessor_element',
        #                       'mat_fober_optic_element', ]
        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()

        new_amount = warehouse.amount + amount_shipment
        Warehouse.objects.filter(user=session_user, user_city=session_user_city, resource_id=shipment_id).update(
            amount=new_amount)
        mass = amount_shipment
        size = amount_shipment

    elif class_shipment == 10:
        warehouse_factory = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                            factory_id=shipment_id).first()
        amount_factory = warehouse_factory.amount
        new_amount = amount_factory + amount_shipment
        warehouse_factory = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                            factory_id=shipment_id).update(amount=new_amount)
        mass = amount_shipment * warehouse_factory.mass
        size = amount_shipment * warehouse_factory.size

    else:
        element = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                  element_class=class_shipment, element_id=shipment_id).first()
        amount_element = element.amount
        new_amount = amount_shipment + amount_element
        WarehouseElement.objects.filter(user=session_user, user_city=session_user_city, element_class=class_shipment,
                                        element_id=shipment_id).update(amount=new_amount)
        hold = Hold.objects.filter(fleet=fleet, class_shipment=class_shipment, shipment_id=shipment_id).first()
        mass = amount_shipment * (hold.mass_shipment / hold.amount_shipment)
        size = amount_shipment * (hold.size_shipment / hold.amount_shipment)

    if hold_amount_shipment == amount_shipment:
        Hold.objects.filter(fleet=fleet, class_shipment=class_shipment, shipment_id=shipment_id).delete()
    else:
        new_amount = hold.amount_shipment - amount_shipment

        new_mass = hold.mass_shipment - amount_shipment * (hold.mass_shipment / hold.amount_shipment)
        new_size = hold.size_shipment - amount_shipment * (hold.size_shipment / hold.amount_shipment)

        Hold.objects.filter(fleet=fleet, class_shipment=class_shipment, shipment_id=shipment_id).update(
            amount_shipment=new_amount, mass_shipment=new_mass, size_shipment=new_size)
    fleet = Fleet.objects.filter(id=fleet).first()
    empty_hold = fleet.empty_hold
    ship_empty_mass = fleet.ship_empty_mass
    new_empty_hold = empty_hold + size
    new_ship_empty_mass = ship_empty_mass - mass
    Fleet.objects.filter(id=fleet.id).update(empty_hold=new_empty_hold, ship_empty_mass=new_ship_empty_mass)
