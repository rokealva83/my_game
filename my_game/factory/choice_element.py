# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, TurnProduction
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, FactoryInstalled, FuelPattern, DevicePattern
from my_game.models import BasicResource
from my_game.models import ManufacturingComplex
from my_game.factory import verification_stage_production
from my_game.building import assembly_line_workpieces


def choice_element(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        verification_stage_production.verification_stage_production(session_user)
        factory_installed = FactoryInstalled.objects.filter(id=request.POST.get('factory_id')).first()
        if not factory_installed:
            factory_installeds = FactoryInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                                 complex_status=0)
            manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
            user_citys = UserCity.objects.filter(user=session_user)
            message = 'Выберите завод'
            request.session['user'] = session_user.id
            request.session['user_city'] = session_user_city.id
            request.session['live'] = True
            output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                      'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs,
                      'factory_installeds': factory_installeds, 'message': message}
            return render(request, "factory.html", output)

        factory_installeds = FactoryInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                             complex_status=0)
        attributes = {}
        element_patterns = {}

        if factory_installed.factory_pattern.production_class == 1:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit",
                "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material", "price_chemical",
                "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "hull_health", "generator", "engine", "weapon", "armor", "shield",
                "main_weapon", "module", "hold_size", "hull_size", "hull_mass", "power_consuption")
            element_patterns = HullPattern.objects.filter(user=session_user).all()
        elif factory_installed.factory_pattern.production_class == 2:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit",
                "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material", "price_chemical",
                "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "armor_health",
                "value_energy_resistance", "value_phisical_resistance", "armor_power", "armor_regeneration",
                "armor_mass")
            element_patterns = ArmorPattern.objects.filter(user=session_user).all()
        elif factory_installed.factory_pattern.production_class == 3:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit", "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material",
                "price_chemical", "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "shield_health", "value_energy_resistance", "value_phisical_resistance",
                "number_of_emitter", "shield_regeneration", "shield_mass", "shield_size", "power_consuption")
            element_patterns = ShieldPattern.objects.filter(user=session_user).all()
        elif factory_installed.factory_pattern.production_class == 4:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit", "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material",
                "price_chemical", "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "engine_health", "system_power", "intersystem_power", "giper_power",
                "nullT_power", "engine_mass", "engine_size", "power_consuption")
            element_patterns = EnginePattern.objects.filter(user=session_user).all()
        elif factory_installed.factory_pattern.production_class == 5:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit", "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material",
                "price_chemical", "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "generator_health", "produced_energy", "fuel_necessary", "generator_mass",
                "generator_size")
            element_patterns = GeneratorPattern.objects.filter(user=session_user).all()
        elif factory_installed.factory_pattern.production_class == 6:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit", "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material",
                "price_chemical", "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "weapon_health", "weapon_energy_damage", "weapon_regenerations",
                "number_of_bursts", "weapon_range", "weapon_accuracy", "weapon_mass", "weapon_size", "power_consuption")
            element_patterns = WeaponPattern.objects.filter(user=session_user).all()

        elif factory_installed.factory_pattern.production_class == 7:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit", "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material",
                "price_chemical", "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "shell_phisical_damage", "shell_speed", "shell_mass", "shell_size")
            element_patterns = ShellPattern.objects.filter(user=session_user).all()

        elif factory_installed.factory_pattern.production_class == 8:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit", "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material",
                "price_chemical", "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "module_health", "param1", "param2", "param3", "module_mass",
                "module_size", "power_consuption")
            element_patterns = ModulePattern.objects.filter(user=session_user).all()

        elif factory_installed.factory_pattern.production_class == 9:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit", "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material",
                "price_chemical", "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "device_health", "produced_energy", "fuel_necessary", "device_mass",
                "device_size", "power_consuption")
            element_patterns = DevicePattern.objects.filter(user=session_user).all()

        elif factory_installed.factory_pattern.production_class == 14:
            attributes = (
                "price_internal_currency", "price_nickel", "price_iron", "price_cooper", "price_aluminum",
                "price_veriarit", "price_inneilit", "price_renniit", "price_cobalt", "price_construction_material",
                "price_chemical", "price_high_strength_allov", "price_nanoelement", "price_microprocessor_element",
                "price_fober_optic_element", "fuel_mass", "fuel_size", "fuel_efficiency")
            element_patterns = FuelPattern.objects.filter(user=session_user).all()

        basic_resources = BasicResource.objects.filter()
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user,
                                                                     user_city=session_user_city).all()
        turn_productions = TurnProduction.objects.filter(user=session_user, user_city=session_user_city).all()
        user_citys = UserCity.objects.filter(user=session_user).all()
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'factory_installeds': factory_installeds, 'factory_installed': factory_installed,
                  'element_patterns': element_patterns, 'attributes': attributes, 'turn_productions': turn_productions,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs,
                  'factory_warehouse': factory_installed.factory_warehouse, 'basic_resources': basic_resources}
        return render(request, "factory.html", output)
