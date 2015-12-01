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
                price_resource1=device_scient.price_resource1,
                price_resource2=device_scient.price_resource2,
                price_resource3=device_scient.price_resource3,
                price_resource4=device_scient.price_resource4,
                price_mineral1=device_scient.price_mineral1,
                price_mineral2=device_scient.price_mineral2,
                price_mineral3=device_scient.price_mineral3,
                price_mineral4=device_scient.price_mineral4,
            )
            device_pattern.save()
            new_factory_pattern(user, 9, device_scient.id)
