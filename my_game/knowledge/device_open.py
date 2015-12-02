# -*- coding: utf-8 -*-

import random
from my_game.models import DevicePattern
from my_game.models import BasicDevice
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern


def device_open(request):
    user = request
    basic_device = BasicDevice.objects.all()
    number_device = len(basic_device) - 1
    number_device_scient = random.randint(0, number_device)
    device_scient = basic_device[number_device_scient]
    user_device = DevicePattern.objects.filter(user=user, basic_device=device_scient).last()
    if user_device is None:
        koef = element_open(user, device_scient)
        if koef < 0:
            koef = 0.00001
        upper_scope = 0.33 * koef
        new_device = random.random()
        if 0 < new_device < upper_scope:
            device_pattern = DevicePattern(
                user=user,
                basic_device=device_scient,
                device_name=device_scient.device_name,
                device_health=device_scient.device_health,
                param1=device_scient.param1,
                param2=device_scient.param2,
                param3=device_scient.param3,
                device_mass=device_scient.device_mass,
                device_size=device_scient.device_size,
                power_consuption=device_scient.power_consuption,
                device_class=device_scient.device_class,
                price_internal_currency=device_scient.price_internal_currency,
                price_nickel=device_scient.price_nickel,
                price_iron=device_scient.price_iron,
                price_cooper=device_scient.price_cooper,
                price_aluminum=device_scient.price_aluminum,
                price_veriarit=device_scient.price_veriarit,
                price_inneilit=device_scient.price_inneilit,
                price_renniit=device_scient.price_renniit,
                price_cobalt=device_scient.price_cobalt,
                price_construction_material=device_scient.price_construction_material,
                price_chemical=device_scient.price_chemical,
                price_high_strength_allov=device_scient.price_high_strength_allov,
                price_nanoelement=device_scient.price_nanoelement,
                price_microprocessor_element=device_scient.price_microprocessor_element,
                price_fober_optic_element=device_scient.price_fober_optic_element
            )
            device_pattern.save()
            new_factory_pattern(user, 9, device_scient.id)
