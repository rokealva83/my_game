# -*- coding: utf-8 -*-
from my_game.models import UserVariables


def price_increase(*args):
    pattern = args[0]
    summary_percent_up = args[1]
    koef_up = (1 + UserVariables.objects.get(id=1).koef_price_increace_modern_element) * (1 + summary_percent_up)
    price_internal_currency = pattern.price_internal_currency * koef_up
    price_nickel = pattern.price_nickel * koef_up
    price_iron = pattern.price_iron * koef_up
    price_cooper = pattern.price_cooper * koef_up
    price_aluminum = pattern.price_aluminum * koef_up
    price_veriarit = pattern.price_veriarit * koef_up
    price_inneilit = pattern.price_inneilit * koef_up
    price_renniit = pattern.price_renniit * koef_up
    price_cobalt = pattern.price_cobalt * koef_up
    price_construction_material = pattern.price_construction_material * koef_up
    price_chemical = pattern.price_chemical * koef_up
    price_high_strength_allov = pattern.price_high_strength_allov * koef_up
    price_nanoelement = pattern.price_nanoelement * koef_up
    price_microprocessor_element = pattern.price_microprocessor_element * koef_up
    price_fober_optic_element = pattern.price_fober_optic_element * koef_up
    setattr(pattern, "price_internal_currency", price_internal_currency)
    setattr(pattern, 'price_nickel', price_nickel)
    setattr(pattern, 'price_iron', price_iron)
    setattr(pattern, 'price_cooper', price_cooper)
    setattr(pattern, 'price_aluminum', price_aluminum)
    setattr(pattern, 'price_veriarit', price_veriarit)
    setattr(pattern, 'price_inneilit', price_inneilit)
    setattr(pattern, 'price_renniit', price_renniit)
    setattr(pattern, 'price_cobalt', price_cobalt)
    setattr(pattern, 'price_construction_material', price_construction_material)
    setattr(pattern, 'price_chemical', price_chemical)
    setattr(pattern, 'price_high_strength_allov', price_high_strength_allov)
    setattr(pattern, 'price_nanoelement', price_nanoelement)
    setattr(pattern, 'price_microprocessor_element', price_microprocessor_element)
    setattr(pattern, 'price_fober_optic_element', price_fober_optic_element)
    pattern.save()
