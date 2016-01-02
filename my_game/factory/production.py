# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, TurnProduction
from my_game.models import FactoryInstalled
from my_game.models import WarehouseFactory
from my_game.models import ManufacturingComplex
from my_game.factory import verification_stage_production
from my_game.building import assembly_line_workpieces
from my_game.factory.rename_element_pattern import rename_element_pattern
from my_game.factory.production_module import production_module
from my_game.factory.production_fuel import production_fuel
from my_game.factory.stop_production import stop_production


def production(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        verification_stage_production.verification_stage_production(session_user)
        message = ''
        if request.POST.get('rename_element_pattern'):
            new_name = request.POST.get('new_name')
            pattern_id = request.POST.get('hidden_factory')
            element_id = request.POST.get('hidden_element')
            message = rename_element_pattern(session_user, session_user_city, pattern_id, element_id, new_name)

        elif request.POST.get('buttom_amount_element'):
            element_id = request.POST.get('hidden_element')
            amount_element = request.POST.get('amount_element')
            factory = FactoryInstalled.objects.filter(id=request.POST.get('hidden_factory')).first()
            if factory.production_class != 14:
                message = production_module(session_user, session_user_city, factory, element_id, amount_element)
            else:
                message = production_fuel(session_user, session_user_city, factory, element_id, amount_element)

        elif request.POST.get('disassembling'):
            factory = FactoryInstalled.objects.filter(id=request.POST.get('hidden_factory')).first()
            turn_production = TurnProduction.objects.filter(factory=factory).first()
            if turn_production:
                message = 'На фабрике идет производство. Удаление невозможно'
            else:
                delete_factory = FactoryInstalled.objects.filter(id=factory.id).first()
                return_factory = WarehouseFactory.objects.filter(factory=factory).first()
                new_amount = return_factory.amount + 1
                WarehouseFactory.objects.filter(factory=factory).update(amount=new_amount)
                new_energy = session_user_city.use_energy - delete_factory.power_consumption
                UserCity.objects.filter(id=session_user_city.id).update(use_energy=new_energy)
                FactoryInstalled.objects.filter(id=factory.id).delete()
                message = 'Фабрика удалена'

        elif request.POST.get('stop_production'):
            turn_id = request.POST.get('hidden_turn_id')
            message = stop_production(turn_id)

        factory_installeds = FactoryInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                             complex_status=0).order_by('production_class',
                                                                                        'production_id')
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user,
                                                                     user_city=session_user_city).all()
        user_city = UserCity.objects.filter(user=session_user).first()
        user_citys = UserCity.objects.filter(user=session_user).all()
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': user_city,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs,
                  'factory_installeds': factory_installeds, 'message': message}

        return render(request, "factory.html", output)
