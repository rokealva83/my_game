from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
import math
import random
import sys
import string
from datetime import datetime, timedelta, date, time as dt_time
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from django.utils import timezone
from models import Galaxy, System, Planet
from models import MyUser, User_city, Race, User_scientic
from models import Warehouse
from models import Basic_scientic, Turn_scientic, Basic_armor, Basic_engine, Basic_factory, Basic_generator, \
    Basic_hull, Basic_module, Basic_shell, Basic_shield, Basic_weapon
from models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern


def check_scientic(request):
    user = int(request)
    time = timezone.now()
    turn_scientic = Turn_scientic.objects.filter(user=user).first()
    if turn_scientic:
        scin_id = turn_scientic.id
        time_start = turn_scientic.start_time_science
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta_time = turn_scientic.finish_time_science - turn_scientic.start_time_science
        delta = delta_time.seconds
        if new_delta > delta:
            scientic = User_scientic.objects.filter(user=user).first()
            all_scient = scientic.mathematics_up + scientic.phisics_up + scientic.biologic_chimics_up + \
                         scientic.energetics_up + scientic.radionics_up + scientic.nanotech_up + \
                         scientic.astronomy_up + scientic.logistic_up
            user_scientic = User_scientic.objects.filter(user=user).update(
                mathematics_up=scientic.mathematics_up + turn_scientic.mathematics_up,
                phisics_up=scientic.phisics_up + turn_scientic.phisics_up,
                biologic_chimics_up=scientic.biologic_chimics_up + turn_scientic.biologic_chimics_up,
                energetics_up=scientic.energetics_up + turn_scientic.energetics_up,
                radionics_up=scientic.radionics_up + turn_scientic.radionics_up,
                nanotech_up=scientic.nanotech_up + turn_scientic.nanotech_up,
                astronomy_up=scientic.astronomy_up + turn_scientic.astronomy_up,
                logistic_up=scientic.logistic_up + turn_scientic.logistic_up,
                all_scientic=all_scient + 1,
            )
            Turn_scientic.objects.filter(id=scin_id).delete()
    all_scientic = User_scientic.objects.filter(user=user).first()
    if all_scientic.all_scientic > 10:
        new_technology = random.random()

        if 0 <= new_technology < 0.125:
            hull_upgrade(user)

        if 0.125 <= new_technology < 0.250:
            armor_upgrade(user)

        if 0.250 <= new_technology < 0.375:
            shield_upgrade(user)

        if 0.375 <= new_technology < 0.5:
            engine_upgrade(user)

        if 0.5 <= new_technology < 0.625:
            generator_upgrade(user)

        if 0.625 <= new_technology < 0.750:
            weapon_upgrade(user)

        if 0.750 <= new_technology < 0.875:
            shell_upgrade(user)

        if 0.875 <= new_technology <= 1:
            module_upgrade(user)


def hull_upgrade(request):
    user = request
    b_hull = Basic_hull.objects.all()
    number_hull = len(b_hull) - 1
    number_hull_scient = random.randint(0, number_hull)
    hull_scient = b_hull[number_hull_scient]
    u_hull = Hull_pattern.objects.filter(user=user, hull=hull_scient.id).last()
    if u_hull is None:
        all_base = int(hull_scient.min_all_scientic)
        scin_user = User_scientic.objects.filter(user=user).first()
        all_user = int(scin_user.all_scientic)

        if all_base < all_user:
            koef_all = (all_user - all_base) / 100.0
        else:
            koef_all = -(all_base - all_user) / 100.0

        math_base = int(hull_scient.min_math)
        math_user = int(scin_user.mathematics_up)
        if math_base < math_user:
            koef_math = (math_user - math_base) / 100.0
        else:
            koef_math = (math_user - math_base) / 100.0

        nano_base = int(hull_scient.min_nanotech)
        nano_user = int(scin_user.nanotech_up)
        if nano_base < nano_user:
            koef_nanotech = (nano_user - nano_base) / 100.0
        else:
            koef_nanotech = -(nano_base - nano_user) / 100.0

        astro_base = int(hull_scient.min_astronomy)
        astro_user = int(scin_user.astronomy_up)
        if astro_base < astro_user:
            koef_astronomy = (astro_user - astro_base) / 100.0
        else:
            koef_astronomy = -(astro_base - astro_user) / 100.0

        luckyness = MyUser.objects.filter(user_id=user).first()
        lucky = luckyness.user_luckyness
        koef = (1 + (koef_all + koef_math + koef_nanotech + koef_astronomy)) * \
               (1 + lucky / 100.0)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_hull = random.random()
        if 0 < new_hull < upper_scope:
            hull_pattern = Hull_pattern(
                user=user,
                hull=hull_scient.id,
                health=hull_scient.health,
                generators=hull_scient.generators,
                engines=hull_scient.engines,
                weapons=hull_scient.weapons,
                armor=hull_scient.armor,
                shield=hull_scient.shield,
                main_weapons=hull_scient.main_weapons,
                hold_size=hull_scient.hold_size,
                mass=hull_scient.mass,
                size=hull_scient.size,
                power_consuption=hull_scient.power_consuption,
            )
            hull_pattern.save()
    else:
        u_hull = Hull_pattern.objects.filter(user=user, hull=hull_scient.id).last()
        hull_atribute = ['health', 'generators', 'engines', 'weapons', 'armor', 'shield', \
                         'main_weapons', 'hold_size', 'mass', 'size', 'power_consuption']
        trying = random.random()
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 10)
            atribute = hull_atribute[number]
            element = getattr(u_hull, atribute)
            last_element = getattr(u_hull, atribute)
            element_basic = getattr(hull_scient, atribute)
            if u_hull.hull == 1:
                if number == 5 and element == 0:
                    element = 1
                else:
                    if number == 8 or number == 10:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        if element / element_basic > 0.7:
                            element = element * percent_update
                            u_hull.pk = None
                            u_hull.save()
                            u_hull = Hull_pattern.objects.filter(user=user, hull=hull_scient.id).last()
                            setattr(u_hull, atribute, element)
                            u_hull.save()
                    if number == 0 or number == 7 or number == 9:
                        percent_update = 1 + random.randint(5, 10) / 100.0
                        if element != 0 and element_basic / element > 0.7:
                            element = element * percent_update
                            u_hull.pk = None
                            u_hull.save()
                            u_hull = Hull_pattern.objects.filter(user=user, hull=hull_scient.id).last()
                            setattr(u_hull, atribute, element)
                            u_hull.save()
                    else:
                        if element != 0 and element / element_basic < 2:
                            element = element + 1
                            u_hull.pk = None
                            u_hull.save()
                            u_hull = Hull_pattern.objects.filter(user=user, hull=hull_scient.id).last()
                            setattr(u_hull, atribute, element)
                            u_hull.save()
            else:
                if element != 0:
                    if number == 8 or number == 10:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        if element / element_basic > 0.7:
                            element = element * percent_update
                            u_hull.pk = None
                            u_hull.save()
                            u_hull = Hull_pattern.objects.filter(user=user, hull=hull_scient.id).last()
                            setattr(u_hull, atribute, element)
                            u_hull.save()
                    else:
                        if number == 0 or number == 7 or number == 9:
                            percent_update = 1 + random.randint(5, 10) / 100.0
                            if element_basic / element > 0.7:
                                element = element * percent_update
                                u_hull.pk = None
                                u_hull.save()
                                u_hull = Hull_pattern.objects.filter(user=user, hull=hull_scient.id).last()
                                setattr(u_hull, atribute, element)
                                u_hull.save()
                        else:
                            if element / element_basic < 2:
                                element = element + 1
                                u_hull.pk = None
                                u_hull.save()
                                u_hull = Hull_pattern.objects.filter(user=user, hull=hull_scient.id).last()
                                setattr(u_hull, atribute, element)
                                u_hull.save()


def armor_upgrade(request):
    user = request
    b_armor = Basic_armor.objects.all()
    number_armor = len(b_armor) - 1
    number_armor_scient = random.randint(0, number_armor)
    armor_scient = b_armor[number_armor_scient]
    u_armor = Armor_pattern.objects.filter(user=user, armor=armor_scient.id).last()
    if u_armor is None:
        all_base = int(armor_scient.min_all_scientic)
        scin_user = User_scientic.objects.filter(user=user).first()
        all_user = int(scin_user.all_scientic)
        if all_base < all_user:
            koef_all = (all_user - all_base) / 100.0
        else:
            koef_all = -(all_base - all_user) / 100.0

        phis_base = int(armor_scient.min_phis)
        phis_user = int(scin_user.phisics_up)
        if phis_base < phis_user:
            koef_phis = (phis_user - phis_base) / 100.0
        else:
            koef_phis = (phis_user - phis_base) / 100.0

        biol_base = int(armor_scient.min_biol)
        biol_user = int(scin_user.biologic_chimics_up)
        if biol_base < biol_user:
            koef_biol = (biol_user - biol_base) / 100.0
        else:
            koef_biol = -(biol_base - biol_user) / 100.0

        logist_base = int(armor_scient.min_logist)
        logist_user = int(scin_user.logistic_up)
        if logist_base < logist_user:
            koef_logist = (logist_user - logist_base) / 100.0
        else:
            koef_logist = -(logist_base - logist_user) / 100.0

        luckyness = MyUser.objects.filter(user_id=user).first()
        lucky = luckyness.user_luckyness
        koef = (1 + (koef_all + koef_phis + koef_biol + koef_logist)) * \
               (1 + lucky / 100.0)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_armor = random.random()
        if 0 < new_armor < upper_scope:
            armor_pattern = Armor_pattern(
                user=user,
                armor=armor_scient.id,
                health=armor_scient.health,
                value_energy_resistance=armor_scient.value_energy_resistance,
                value_phisical_resistance=armor_scient.value_phisical_resistance,
                regeneration=armor_scient.regeneration,
                power=armor_scient.power,
                mass=armor_scient.mass,
            )
            armor_pattern.save()
    else:
        u_armor = Armor_pattern.objects.filter(user=user, armor=armor_scient.id).last()
        armor_atribute = ['health', 'value_energy_resistance', 'value_phisical_resistance', 'regeneration', 'power',
                          'mass']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0

        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 5)
            atribute = armor_atribute[number]
            element = getattr(u_armor, atribute)
            last_element = getattr(u_armor, atribute)
            element_basic = getattr(armor_scient, atribute)

            if element != 0:
                if number == 5:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_armor.pk = None
                        u_armor.save()
                        u_armor = Armor_pattern.objects.filter(user=user, armor=armor_scient.id).last()
                        setattr(u_armor, atribute, element)
                        u_armor.save()
                else:
                    ell = element_basic / element
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_armor.pk = None
                        u_armor.save()
                        u_armor = Armor_pattern.objects.filter(user=user, armor=armor_scient.id).last()
                        setattr(u_armor, atribute, element)
                        u_armor.save()


def shield_upgrade(request):
    user = request
    b_shield = Basic_shield.objects.all()
    number_shield = len(b_shield) - 1
    number_shield_scient = random.randint(0, number_shield)
    shield_scient = b_shield[number_shield_scient]
    u_shield = Shield_pattern.objects.filter(user=user, shield=shield_scient.id).last()
    if u_shield is None:
        all_base = int(shield_scient.min_all_scientic)
        scin_user = User_scientic.objects.filter(user=user).first()
        all_user = int(scin_user.all_scientic)
        if all_base < all_user:
            koef_all = (all_user - all_base) / 100.0
        else:
            koef_all = -(all_base - all_user) / 100.0

        phis_base = int(shield_scient.min_phis)
        phis_user = int(scin_user.phisics_up)
        if phis_base < phis_user:
            koef_phis = (phis_user - phis_base) / 100.0
        else:
            koef_phis = (phis_user - phis_base) / 100.0

        energy_base = int(shield_scient.min_energy)
        energy_user = int(scin_user.energetics_up)
        if energy_base < energy_user:
            koef_energy = (energy_user - energy_base) / 100.0
        else:
            koef_energy = (energy_user - energy_base) / 100.0

        nanotech_base = int(shield_scient.min_nanotech)
        nanotech_user = int(scin_user.nanotech_up)
        if nanotech_base < nanotech_user:
            koef_nanotech = (nanotech_user - nanotech_base) / 100.0
        else:
            koef_nanotech = (nanotech_user - nanotech_base) / 100.0
        luckyness = MyUser.objects.filter(user_id=user).first()
        lucky = luckyness.user_luckyness
        koef = (1 + (koef_all + koef_phis + koef_energy + koef_nanotech)) * \
               (1 + lucky / 100)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_shield = random.random()
        if 0 < new_shield < upper_scope:
            shield_pattern = Shield_pattern(
                user=user,
                shield=shield_scient.id,
                health=shield_scient.health,
                value_energy_resistance=shield_scient.value_energy_resistance,
                value_phisical_resistance=shield_scient.value_phisical_resistance,
                regeneration=shield_scient.regeneration,
                number_of_emitter=shield_scient.number_of_emitter,
                mass=shield_scient.mass,
                size=shield_scient.size,
                power_consuption=shield_scient.power_consuption,
            )
            shield_pattern.save()
    else:
        shield_atribute = ['health', 'value_energy_resistance', 'value_phisical_resistance', 'regeneration', \
                           'number_of_emitter', 'mass', 'size', 'power_consuption']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 7)
            atribute = shield_atribute[number]
            element = getattr(u_shield, atribute)
            element_basic = getattr(shield_scient, atribute)
            last_element = getattr(u_shield, atribute)
            if element != 0:
                if number == 5 or number == 7:
                    if element / element_basic > 0.7:
                        percent_update = 1.0 - random.randint(5, 10)/100.0
                        element = element * percent_update
                        u_shield.pk = None
                        u_shield.save()
                        u_shield = Shield_pattern.objects.filter(user=user, shield=shield_scient.id).last()
                        setattr(u_shield, atribute, element)
                        u_shield.save()
                else:
                    if number == 4:
                        if element_basic / element > 0.5:
                            element = element + 1
                            u_shield.pk = None
                            u_shield.save()
                            u_shield = Shield_pattern.objects.filter(user=user, shield=shield_scient.id).last()
                            setattr(u_shield, atribute, element)
                            u_shield.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            u_shield.pk = None
                            u_shield.save()
                            u_shield = Shield_pattern.objects.filter(user=user, shield=shield_scient.id).last()
                            setattr(u_shield, atribute, element)
                            u_shield.save()


def engine_upgrade(request):
    user = request
    b_engine = Basic_engine.objects.all()
    number_engine = len(b_engine)-1
    number_engine_scient = random.randint(0, number_engine)
    engine_scient = b_engine[number_engine_scient]
    u_engine = Engine_pattern.objects.filter(user=user, engine=engine_scient.id).last()
    if u_engine is None:

        all_base=int(engine_scient.min_all_scientic)
        scin_user = User_scientic.objects.filter(user=user).first()
        all_user = int(scin_user.all_scientic)
        if all_base < all_user:
            koef_all = (all_user - all_base)/100.0
        else:
            koef_all = -(all_base - all_user)/100.0

        phis_base = int(engine_scient.min_phis)
        phis_user = int(scin_user.phisics_up)
        if phis_base < phis_user:
            koef_phis = (phis_user - phis_base) / 100.0
        else:
            koef_phis = (phis_user - phis_base) / 100.0

        biol_base = int(engine_scient.min_biol)
        biol_user = int(scin_user.biologic_chimics_up)
        if biol_base < biol_user:
            koef_biol = (biol_user - biol_base) / 100.0
        else:
            koef_biol = -(biol_base - biol_user) / 100.0

        energy_base = int(engine_scient.min_energy)
        energy_user = int(scin_user.energetics_up)
        if energy_base < energy_user:
            koef_energy = (energy_user - energy_base) / 100.0
        else:
            koef_energy = (energy_user - energy_base) / 100.0

        nanotech_base = int(engine_scient.min_nanotech)
        nanotech_user = int(scin_user.nanotech_up)
        if nanotech_base < nanotech_user:
            koef_nanotech = (nanotech_user - nanotech_base) / 100.0
        else:
            koef_nanotech = (nanotech_user - nanotech_base) / 100.0
        luckyness = MyUser.objects.filter(user_id=user).first()
        lucky = luckyness.user_luckyness

        koef = (1 + (koef_all + koef_phis + koef_biol + koef_energy + koef_nanotech)) * \
               (1 + lucky / 100.0)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_engine = random.random()
        if 0 < new_engine < upper_scope:
            engine_pattern = Engine_pattern(
                user=user,
                engine=engine_scient.id,
                health=engine_scient.health,
                system_power=engine_scient.system_power,
                intersystem_power=engine_scient.intersystem_power,
                giper_power=engine_scient.giper_power,
                nullT_power=engine_scient.nullT_power,
                mass=engine_scient.mass,
                size=engine_scient.size,
                power_consuption=engine_scient.power_consuption,
            )
            engine_pattern.save()
    else:
        u_engine = Engine_pattern.objects.filter(user=user, engine=engine_scient.id).last()
        engine_atribute = ['health', 'system_power', 'intersystem_power', 'giper_power', \
                           'nullT_power', 'mass', 'size', 'power_consuption']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(1, 7)
            atribute = engine_atribute[number]
            element = getattr(u_engine, atribute)
            last_element = getattr(u_engine, atribute)
            element_basic = getattr(engine_scient, atribute)
            if element !=0:
                if number == 5 or number == 6 or number == 7:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_engine.pk = None
                        u_engine.save()
                        u_engine = Engine_pattern.objects.filter(user=user, engine=engine_scient.id).last()
                        setattr(u_engine, atribute, element)
                        u_engine.save()
                else:
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_engine.pk = None
                        u_engine.save()
                        u_engine = Engine_pattern.objects.filter(user=user, engine=engine_scient.id).last()
                        setattr(u_engine, atribute, element)
                        u_engine.save()


def generator_upgrade(request):
    user = request
    b_generator = Basic_generator.objects.all()
    number_generator = len(b_generator)-1
    number_generator_scient = random.randint(0, number_generator)
    generator_scient = b_generator[number_generator_scient]
    u_generator = Generator_pattern.objects.filter(user=user, generator=generator_scient.id).last()
    if u_generator is None:

        all_base = int(generator_scient.min_all_scientic)
        scin_user = User_scientic.objects.filter(user=user).first()
        all_user = int(scin_user.all_scientic)
        if all_base < all_user:
            koef_all = (all_user - all_base) / 100.0
        else:
            koef_all = -(all_base - all_user) / 100.0

        phis_base = int(generator_scient.min_phis)
        phis_user = int(scin_user.phisics_up)
        if phis_base < phis_user:
            koef_phis = (phis_user - phis_base) / 100.0
        else:
            koef_phis = (phis_user - phis_base) / 100.0

        energy_base = int(generator_scient.min_energy)
        energy_user = int(scin_user.energetics_up)
        if energy_base < energy_user:
            koef_energy = (energy_user - energy_base) / 100.0
        else:
            koef_energy = (energy_user - energy_base) / 100.0

        nano_base = int(generator_scient.min_nanotech)
        nano_user = int(scin_user.nanotech_up)
        if nano_base < nano_user:
            koef_nanotech = (nano_user - nano_base) / 100.0
        else:
            koef_nanotech = -(nano_base - nano_user) / 100.0

        luckyness = MyUser.objects.filter(user_id=user).first()
        lucky =  luckyness.user_luckyness
        koef = (1 + (koef_all + koef_phis + koef_energy + koef_nanotech)) * \
               (1 + lucky / 100.0)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_generator = random.random()
        if 0 < new_generator < upper_scope:
            generator_pattern = Generator_pattern(
                user=user,
                generator=generator_scient.id,
                health=generator_scient.health,
                produced_energy=generator_scient.produced_energy,
                fuel_necessary=generator_scient.fuel_necessary,
                mass=generator_scient.mass,
                size=generator_scient.size,
            )
            generator_pattern.save()
    else:
        generator_atribute = ['health', 'produced_energy', 'fuel_necessary', 'mass', 'size']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 4)
            atribute = generator_atribute[number]
            element = getattr(u_generator, atribute)
            last_element = getattr(u_generator, atribute)
            element_basic = getattr(generator_scient, atribute)
            if element !=0:
                if number == 2 or number == 3 or number == 4:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_generator.pk = None
                        u_generator.save()
                        u_generator = Generator_pattern.objects.filter(user=user, generator=generator_scient.id).last()
                        setattr(u_generator, atribute, element)
                        u_generator.save()
                else:
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_generator.pk = None
                        u_generator.save()
                        u_generator = Generator_pattern.objects.filter(user=user, generator=generator_scient.id).last()
                        setattr(u_generator, atribute, element)
                        u_generator.save()


def weapon_upgrade(request):
    user = request
    b_weapon = Basic_weapon.objects.all()
    number_weapon = len(b_weapon)-1
    number_weapon_scient = random.randint(0, number_weapon)
    weapon_scient = b_weapon[number_weapon_scient]
    u_weapon = Weapon_pattern.objects.filter(user=user, weapon=weapon_scient.id).last()
    if u_weapon is None:

        all_base = int(weapon_scient.min_all_scientic)
        scin_user = User_scientic.objects.filter(user=user).first()
        all_user = int(scin_user.all_scientic)

        if all_base < all_user:
            koef_all = (all_user - all_base) / 100.0
        else:
            koef_all = -(all_base - all_user) / 100.0

        math_base = int(weapon_scient.min_math)
        math_user = int(scin_user.mathematics_up)
        if math_base < math_user:
            koef_math = (math_user - math_base) / 100.0
        else:
            koef_math = (math_user - math_base) / 100.0

        radio_base = int(weapon_scient.min_radio)
        radio_user = int(scin_user.radionics_up)
        if radio_base < radio_user:
            koef_radio = (radio_user - radio_base) / 100.0
        else:
            koef_radio = (radio_user - radio_base) / 100.0

        nano_base = int(weapon_scient.min_nanotech)
        nano_user = int(scin_user.nanotech_up)
        if nano_base < nano_user:
            koef_nanotech = (nano_user - nano_base) / 100.0
        else:
            koef_nanotech = -(nano_base - nano_user) / 100.0

        logist_base = int(weapon_scient.min_logist)
        logist_user = int(scin_user.logistic_up)
        if logist_base < logist_user:
            koef_logist = (logist_user - logist_base) / 100.0
        else:
            koef_logist = -(logist_base - logist_user) / 100.0

        luckyness = MyUser.objects.filter(user_id=user).first()
        lucky =  luckyness.user_luckyness
        koef = (1 + (koef_all + koef_math + koef_radio + koef_nanotech + koef_logist)) * \
               (1 + lucky / 100.0)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_weapon = random.random()
        if 0 < new_weapon < upper_scope:
            weapon_pattern = Weapon_pattern(
                user=user,
                weapon=weapon_scient.id,
                health=weapon_scient.health,
                energy_damage=weapon_scient.energy_damage,
                regenerations=weapon_scient.regenerations,
                number_of_bursts=weapon_scient.number_of_bursts,
                range=weapon_scient.range,
                accuracy=weapon_scient.accuracy,
                mass=weapon_scient.mass,
                size=weapon_scient.size,
                power_consuption=weapon_scient.power_consuption,
            )
            weapon_pattern.save()

    else:
        u_weapon = Weapon_pattern.objects.filter(user=user, weapon=weapon_scient.id).last()
        weapon_atribute = ['health', 'energy_damage', 'regenerations', 'number_of_bursts', \
                           'range', 'accuracy', 'mass', 'size', 'power_consuption']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7  <= trying <= 0.85:
            number = random.randint(0, 8)
            atribute = weapon_atribute[number]
            element = getattr(u_weapon, atribute)
            last_element = getattr(u_weapon, atribute)
            element_basic = getattr(weapon_scient, atribute)
            if element !=0:
                if number == 6 or number == 7 or number == 8:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_weapon.pk = None
                        u_weapon.save()
                        u_weapon = Weapon_pattern.objects.filter(user=user, weapon=weapon_scient.id).last()
                        setattr(u_weapon, atribute, element)
                        u_weapon.save()
                else:
                    if number == 3 and element / element_basic < 2:
                        element = element + 1
                        u_weapon.pk = None
                        u_weapon.save()
                        u_weapon = Weapon_pattern.objects.filter(user=user, weapon=weapon_scient.id).last()
                        setattr(u_weapon, atribute, element)
                        u_weapon.save()
                    else:
                        if number == 5:
                            if element_basic / element > 0.75:
                                element = element * percent_update
                                u_weapon.pk = None
                                u_weapon.save()
                                u_weapon = Weapon_pattern.objects.filter(user=user, weapon=weapon_scient.id).last()
                                setattr(u_weapon, atribute, element)
                                u_weapon.save()
                        else:
                            if element_basic / element > 0.7:
                                element = element * percent_update
                                u_weapon.pk = None
                                u_weapon.save()
                                u_weapon = Weapon_pattern.objects.filter(user=user, weapon=weapon_scient.id).last()
                                setattr(u_weapon, atribute, element)
                                u_weapon.save()


def shell_upgrade(request):
    user = request
    b_shell = Basic_shell.objects.all()
    number_shell = len(b_shell)-1
    number_shell_scient = random.randint(0, number_shell)
    shell_scient = b_shell[number_shell_scient]
    u_shell = Shell_pattern.objects.filter(user=user, shell=shell_scient.id).last()
    if u_shell is None:

        all_base = int(shell_scient.min_all_scientic)
        scin_user = User_scientic.objects.filter(user=user).first()
        all_user = int(scin_user.all_scientic)

        if all_base < all_user:
            koef_all = (all_user - all_base) / 100.0
        else:
            koef_all = -(all_base - all_user) / 100.0


        radio_base = int(shell_scient.min_radio)
        radio_user = int(scin_user.radionics_up)
        if radio_base < radio_user:
            koef_radio = (radio_user - radio_base) / 100.0
        else:
            koef_radio = (radio_user - radio_base) / 100.0

        astro_base = int(shell_scient.min_astronomy)
        astro_user = int(scin_user.astronomy_up)
        if astro_base < astro_user:
            koef_astronomy = (astro_user - astro_base) / 100.0
        else:
            koef_astronomy = -(astro_base - astro_user) / 100.0

        luckyness = MyUser.objects.filter(user_id=user).first()
        lucky =  luckyness.user_luckyness
        koef = (1 + (koef_all + koef_radio + koef_astronomy)) * \
               (1 + lucky / 100.0)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_shell = random.random()
        if 0 < new_shell < upper_scope:
            shell_pattern = Shell_pattern(
                user=user,
                shell=shell_scient.id,
                phisical_damage=shell_scient.phisical_damage,
                speed=shell_scient.speed,
                mass=shell_scient.mass,
                size=shell_scient.size,
            )
            shell_pattern.save()
    else:
        shell_atribute = ['phisical_damage', 'speed', 'mass', 'size']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15  <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 3)
            atribute = shell_atribute[number]
            element = getattr(u_shell, atribute)
            last_element = getattr(u_shell, atribute)
            element_basic = getattr(shell_scient, atribute)
            if element !=0:
                if number == 2 or number == 3:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_shell.pk = None
                        u_shell.save()
                        u_shell = Shell_pattern.objects.filter(user=user, shell=shell_scient.id).last()
                        setattr(u_shell, atribute, element)
                        u_shell.save()
                else:
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_shell.pk = None
                        u_shell.save()
                        u_shell = Shell_pattern.objects.filter(user=user, shell=shell_scient.id).last()
                        setattr(u_shell, atribute, element)
                        u_shell.save()


def module_upgrade(request):
    user = request
    b_module = Basic_module.objects.all()
    number_module = len(b_module)-1
    number_module_scient = random.randint(0, number_module)
    module_scient = b_module[number_module_scient]
    u_module = Module_pattern.objects.filter(user=user, module=module_scient.id).last()
    if u_module is None:
        all_base = int(module_scient.min_all_scientic)
        scin_user = User_scientic.objects.filter(user=user).first()
        all_user = int(scin_user.all_scientic)
        if all_base < all_user:
            koef_all = (all_user - all_base) / 100.0
        else:
            koef_all = -(all_base - all_user) / 100.0

        math_base = int(module_scient.min_math)
        math_user = int(scin_user.mathematics_up)
        if math_base < math_user:
            koef_math = (math_user - math_base) / 100.0
        else:
            koef_math = (math_user - math_base) / 100.0

        biol_base = int(module_scient.min_biol)
        biol_user = int(scin_user.biologic_chimics_up)
        if biol_base < biol_user:
            koef_biol = (biol_user - biol_base) / 100.0
        else:
            koef_biol = -(biol_base - biol_user) / 100.0

        radio_base = int(module_scient.min_radio)
        radio_user = int(scin_user.radionics_up)
        if radio_base < radio_user:
            koef_radio = (radio_user - radio_base) / 100.0
        else:
            koef_radio = (radio_user - radio_base) / 100.0

        astro_base = int(module_scient.min_astronomy)
        astro_user = int(scin_user.astronomy_up)
        if astro_base < astro_user:
            koef_astronomy = (astro_user - astro_base) / 100.0
        else:
            koef_astronomy = -(astro_base - astro_user) / 100.0

        logist_base = int(module_scient.min_logist)
        logist_user = int(scin_user.logistic_up)
        if logist_base < logist_user:
            koef_logist = (logist_user - logist_base) / 100.0
        else:
            koef_logist = -(logist_base - logist_user) / 100.0

        luckyness = MyUser.objects.filter(user_id=user).first()
        lucky =  luckyness.user_luckyness
        koef = (1 + (koef_all + koef_math + koef_biol + koef_radio + koef_astronomy + koef_logist)) * \
               (1 + lucky / 100.0)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_module = random.random()
        if 0 < new_module < upper_scope:
            module_pattern = Module_pattern(
                user=user,
                module=module_scient.id,
                health=module_scient.health,
                param1=module_scient.param1,
                param2=module_scient.param2,
                param3=module_scient.param3,
                mass=module_scient.mass,
                size=module_scient.size,
                power_consuption=module_scient.power_consuption,
                module_class=module_scient.module_class,
            )
            module_pattern.save()
    else:
        module_atribute = ['health', 'param1', 'param2', 'param3', 'mass', 'size', 'power_consuption']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <=  0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 6)
            atribute = module_atribute[number]
            element = getattr(u_module, atribute)
            last_element = getattr(u_module, atribute)
            element_basic = getattr(module_scient, atribute)
            if element != 0:
                if number == 4 or number == 5 or number == 6:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_module.pk = None
                        u_module.save()
                        u_module = Module_pattern.objects.filter(user=user, module=module_scient.id).last()
                        setattr(u_module, atribute, element)
                        u_module.save()
                else:
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_module.pk = None
                        u_module.save()
                        u_module = Module_pattern.objects.filter(user=user, module=module_scient.id).last()
                        setattr(u_module, atribute, element)
                        u_module.save()
