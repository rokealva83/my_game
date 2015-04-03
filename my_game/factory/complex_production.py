# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Turn_production
from my_game.models import Manufacturing_complex
from my_game.factory import factory_function
from my_game.building import assembly_line_workpieces



def complex_production(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        message = ''
        factory_id = request.POST.get('hidden_factory')
        element_id = request.POST.get('hidden_element')
        amount_element = request.POST.get('amount_element')
        message = factory_function.production_module(session_user, session_user_city, factory_id, element_id,
                                                     amount_element)

        turn_productions = Turn_production.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = Manufacturing_complex.objects.filter(user=session_user, user_city=session_user_city)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'message': message,
                  'turn_productions': turn_productions, 'user_citys': user_citys,
                  'manufacturing_complexs': manufacturing_complexs}
        return render(request, "factory.html", output)
