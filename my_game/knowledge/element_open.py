# -*- coding: utf-8 -*-


def element_open(*args):
    user = args[0]
    element_scient = args[1]
    all_base = int(element_scient.min_all_scientic)
    all_user = int(user.all_scientic)
    if all_base < all_user:
        koef_all = (all_user - all_base) / 100.0
    else:
        koef_all = -(all_base - all_user) / 100.0
    math_base = int(element_scient.min_math)
    math_user = int(user.mathematics_up)
    if math_base != 0:
        if math_base < math_user:
            koef_math = (math_user - math_base) / 100.0
        else:
            koef_math = (math_user - math_base) / 100.0
    else:
        koef_math = 0
    phis_base = int(element_scient.min_phis)
    phis_user = int(user.phisics_up)
    if phis_base != 0:
        if phis_base < phis_user:
            koef_phis = (phis_user - phis_base) / 100.0
        else:
            koef_phis = (phis_user - phis_base) / 100.0
    else:
        koef_phis = 0
    biol_base = int(element_scient.min_biol)
    biol_user = int(user.biologic_chimics_up)
    if biol_base != 0:
        if biol_base < biol_user:
            koef_biol = (biol_user - biol_base) / 100.0
        else:
            koef_biol = -(biol_base - biol_user) / 100.0
    else:
        koef_biol = 0
    energy_base = int(element_scient.min_energy)
    energy_user = int(user.energetics_up)
    if energy_base != 0:
        if energy_base < energy_user:
            koef_energy = (energy_user - energy_base) / 100.0
        else:
            koef_energy = (energy_user - energy_base) / 100.0
    else:
        koef_energy = 0
    radio_base = int(element_scient.min_radio)
    radio_user = int(user.radionics_up)
    if radio_base != 0:
        if radio_base < radio_user:
            koef_radio = (radio_user - radio_base) / 100.0
        else:
            koef_radio = (radio_user - radio_base) / 100.0
    else:
        koef_radio = 0
    nano_base = int(element_scient.min_nanotech)
    nano_user = int(user.nanotech_up)
    if nano_base != 0:
        if nano_base < nano_user:
            koef_nanotech = (nano_user - nano_base) / 100.0
        else:
            koef_nanotech = -(nano_base - nano_user) / 100.0
    else:
        koef_nanotech = 0
    astro_base = int(element_scient.min_astronomy)
    astro_user = int(user.astronomy_up)
    if astro_base != 0:
        if astro_base < astro_user:
            koef_astronomy = (astro_user - astro_base) / 100.0
        else:
            koef_astronomy = -(astro_base - astro_user) / 100.0
    else:
        koef_astronomy = 0
    logist_base = int(element_scient.min_logist)
    logist_user = int(user.logistic_up)
    if logist_base != 0:
        if logist_base < logist_user:
            koef_logist = (logist_user - logist_base) / 100.0
        else:
            koef_logist = -(logist_base - logist_user) / 100.0
    else:
        koef_logist = 0
    lucky = user.user_luckyness
    koefitsient = (1 + (
        koef_all + koef_math + koef_phis + koef_biol + koef_energy + koef_radio + koef_nanotech + koef_astronomy + koef_logist)) * (
                      1 + lucky / 100.0)
    return koefitsient
