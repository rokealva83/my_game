# -*- coding: utf-8 -*-

from my_game.models import FactoryPattern
from my_game.models import BasicFactory


def new_factory_pattern(*args):
    user = args[0]
    production_class = int(args[1])
    production_id = args[2]
    new_factory = BasicFactory.objects.filter(production_class=production_class, production_id=production_id).first()
    user_factory = FactoryPattern(
        user=user,
        basic_factory=new_factory,
        factory_name=new_factory.factory_name,
        price_internal_currency=new_factory.price_internal_currency,
        price_construction_material = new_factory.price_construction_material,
        price_chemical = new_factory.price_chemical,
        price_high_strength_allov = new_factory.price_high_strength_allov,
        price_nanoelement = new_factory.price_nanoelement,
        price_microprocessor_element = new_factory.price_microprocessor_element,
        price_fober_optic_element =new_factory.price_fober_optic_element,
        cost_expert_deployment=new_factory.cost_expert_deployment,
        assembly_workpiece=new_factory.assembly_workpiece,
        time_deployment=new_factory.time_deployment,
        production_class=new_factory.production_class,
        production_id=new_factory.production_id,
        time_production=new_factory.time_production,
        factory_size=new_factory.factory_size,
        factory_mass=new_factory.factory_mass,
        power_consumption=new_factory.power_consumption
    )
    user_factory.save()
    return ()
