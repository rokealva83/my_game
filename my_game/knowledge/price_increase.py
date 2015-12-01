# -*- coding: utf-8 -*-


def price_increase(*args):
    pattern = args[0]
    koef_up = 1.10
    price_internal_currency = pattern.price_internal_currency * koef_up
    price_resource1 = pattern.price_resource1 * koef_up
    price_resource2 = pattern.price_resource2 * koef_up
    price_resource3 = pattern.price_resource3 * koef_up
    price_resource4 = pattern.price_resource4 * koef_up
    price_mineral1 = pattern.price_mineral1 * koef_up
    price_mineral2 = pattern.price_mineral2 * koef_up
    price_mineral3 = pattern.price_mineral3 * koef_up
    price_mineral4 = pattern.price_mineral4 * koef_up
    setattr(pattern, "price_internal_currency", price_internal_currency)
    setattr(pattern, 'price_resource1', price_resource1)
    setattr(pattern, 'price_resource2', price_resource2)
    setattr(pattern, 'price_resource3', price_resource3)
    setattr(pattern, 'price_resource4', price_resource4)
    setattr(pattern, 'price_mineral1', price_mineral1)
    setattr(pattern, 'price_mineral2', price_mineral2)
    setattr(pattern, 'price_mineral3', price_mineral3)
    setattr(pattern, 'price_mineral4', price_mineral4)
    pattern.save()
