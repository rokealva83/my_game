# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Turn_production
from my_game.models import Factory_installed
from my_game.models import Warehouse_factory
from my_game.models import Manufacturing_complex
from my_game.factory import factory_function, verification_stage_production
from my_game.building import assembly_line_workpieces


def production(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        verification_stage_production.verification_stage_production(session_user)
        message = ''
        if request.POST.get('rename_element_pattern'):
            new_name = request.POST.get('new_name')
            pattern_id = request.POST.get('hidden_factory')
            element_id = request.POST.get('hidden_element')
            message = factory_function.rename_element_pattern(session_user, session_user_city, pattern_id, element_id,
                                                              new_name)

        if request.POST.get('buttom_amount_element'):
            factory_id = request.POST.get('hidden_factory')
            element_id = request.POST.get('hidden_element')
            amount_element = request.POST.get('amount_element')
            message = factory_function.production_module(session_user, session_user_city, factory_id, element_id,
                                                         amount_element)

        if request.POST.get('disassembling'):
            factory_id = request.POST.get('hidden_factory')
            turn_production = Turn_production.objects.filter(factory_id=factory_id).first()
            user_city = User_city.objects.filter(id=session_user_city).first()
            if turn_production:
                message = 'На фабрике идет производство. Удаление невозможно'
            else:
                delete_factory = Factory_installed.objects.filter(id=factory_id).first()
                return_factory = Warehouse_factory.objects.filter(factory_id=delete_factory.factory_pattern_id).first()
                new_amount = return_factory.amount + 1
                return_factory = Warehouse_factory.objects.filter(factory_id=delete_factory.factory_pattern_id).update(
                    amount=new_amount)
                new_energy = user_city.use_energy - delete_factory.power_consumption
                user_city = User_city.objects.filter(id=session_user_city).update(use_energy=new_energy)
                delete_factory = Factory_installed.objects.filter(id=factory_id).delete()
                message = 'Фабрика удалена'

        factory_installeds = Factory_installed.objects.filter(user=session_user, user_city=session_user_city,
                                                              complex_status=0).order_by('production_class',
                                                                                         'production_id')
        manufacturing_complexs = Manufacturing_complex.objects.filter(user=session_user, user_city=session_user_city)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'manufacturing_complexs': manufacturing_complexs, 'factory_installeds': factory_installeds}

        return render(request, "factory.html", output)