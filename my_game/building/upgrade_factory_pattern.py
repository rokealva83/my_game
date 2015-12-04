# -*- coding: utf-8 -*-

from my_game.models import FactoryPattern, BuildingPattern


# Улучшение шаблона
def upgrade_factory_pattern(*args):
    pattern_id = int(args[2])
    class_id = int(args[3])
    if class_id != 13:
        old_pattern = FactoryPattern.objects.filter(id=pattern_id).first()
    else:
        old_pattern = BuildingPattern.objects.filter(id=pattern_id).first()
    number = int(args[0])
    if old_pattern.production_class == 12 or old_pattern.production_class == 14:
        speed = 1
    else:
        speed = int(args[1])

    if speed == 1:
        koef_speed = 1
    else:
        koef_speed = int(speed) * 1.6

    if number == 1:
        koef_number = 1
    elif old_pattern.production_class == 13:
        koef_number = int(number)
    else:
        koef_number = int(number) * 1.6

    if class_id != 14:
        new_pattern = FactoryPattern(
            user=old_pattern.user,
            basic_factory=old_pattern.basic_factory,
            factory_name=old_pattern.factory_name,
            price_internal_currency=old_pattern.price_internal_currency * koef_speed * koef_number,
            price_construction_material=old_pattern.price_construction_material * koef_speed * koef_number,
            price_chemical=old_pattern.price_chemical * koef_speed * koef_number,
            price_high_strength_allov=old_pattern.price_high_strength_allov * koef_speed * koef_number,
            price_nanoelement=old_pattern.price_nanoelement * koef_speed * koef_number,
            price_microprocessor_element=old_pattern.price_microprocessor_element * koef_speed * koef_number,
            price_fober_optic_element=old_pattern.price_fober_optic_element * koef_speed * koef_number,
            cost_expert_deployment=old_pattern.cost_expert_deployment * koef_speed * koef_number,
            assembly_workpiece=old_pattern.assembly_workpiece * koef_speed * koef_number,
            time_deployment=old_pattern.time_deployment * koef_speed * koef_number,
            production_class=old_pattern.production_class,
            production_id=old_pattern.production_id,
            time_production=old_pattern.time_production / (speed * number),
            factory_size=old_pattern.factory_size * koef_speed * koef_number / 3,
            factory_mass=old_pattern.factory_mass * koef_speed * koef_number / 3,
            power_consumption=old_pattern.power_consumption * koef_speed * koef_number / 3,
        )
        new_pattern.save()
        new_pattern_id = new_pattern.pk
    else:
        new_pattern = BuildingPattern(
            user=old_pattern.user,
            basic_id=old_pattern.basic_id,
            name=old_pattern.name,
            price_internal_currency=old_pattern.price_internal_currency * koef_speed * koef_number,
            price_construction_material=old_pattern.price_construction_material * koef_speed * koef_number,
            price_chemical=old_pattern.price_chemical * koef_speed * koef_number,
            price_high_strength_allov=old_pattern.price_high_strength_allov * koef_speed * koef_number,
            price_nanoelement=old_pattern.price_nanoelement * koef_speed * koef_number,
            price_microprocessor_element=old_pattern.price_microprocessor_element * koef_speed * koef_number,
            price_fober_optic_element=old_pattern.price_fober_optic_element * koef_speed * koef_number,
            cost_expert_deployment=old_pattern.cost_expert_deployment * koef_speed * koef_number,
            assembly_workpiece=old_pattern.assembly_workpiece * koef_speed * koef_number,
            time_deployment=old_pattern.time_deployment * koef_speed * koef_number,
            production_class=old_pattern.production_class,
            production_id=old_pattern.production_id,
            time_production=old_pattern.time_production / speed,
            size=old_pattern.size * koef_speed * koef_number / 3,
            mass=old_pattern.mass * koef_speed * koef_number / 3,
            power_consumption=old_pattern.power_consumption * koef_speed * koef_number / 3,
            max_warehouse=old_pattern.max_warehouse * koef_number,
            warehouse=old_pattern.warehouse * koef_number,
        )
        new_pattern.save()
        new_pattern_id = new_pattern.pk
    if new_pattern.production_class == 12:
        old_pattern_power = old_pattern.power_consumption
        new_power_consumption = old_pattern_power * number
        FactoryPattern.objects.filter(id=new_pattern_id).update(power_consumption=new_power_consumption)
    message = 'Шаблон улучшен'
    return message
