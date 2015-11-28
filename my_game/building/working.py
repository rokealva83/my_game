# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, TurnBuilding, TurnAssemblyPieces
from my_game.models import ManufacturingComplex
from my_game.building import assembly_line_workpieces
from my_game.building.delete_factory_pattern import delete_factory_pattern
from my_game.building.install_factory_unit import install_factory_unit
from my_game.building.making_factory_unit import making_factory_unit
from my_game.building.rename_factory_pattern import rename_factory_pattern
from my_game.building.upgrade_factory_pattern import upgrade_factory_pattern


def working(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        message = ''

        if request.POST.get('rename_factory_pattern') is not None:
            new_name = request.POST.get('rename_factory_pattern')
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = rename_factory_pattern(new_name, pattern_id, class_id)

        if request.POST.get('upgrade_factory_pattern') is not None:
            number = request.POST.get('number')
            speed = request.POST.get('speed')
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = upgrade_factory_pattern(number, speed, pattern_id, class_id)

        if request.POST.get('delete_factory_pattern') is not None:
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = delete_factory_pattern(pattern_id, class_id)

        if request.POST.get('making_factory_unit') is not None:
            amount_factory_unit = request.POST.get('amount_factory')
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = making_factory_unit(session_user, session_user_city, amount_factory_unit,
                                          pattern_id, class_id)

        if request.POST.get('install_factory_unit') is not None:
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = install_factory_unit(session_user, session_user_city, pattern_id, class_id)

        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        user_citys = UserCity.objects.filter(user=session_user)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'message': message, 'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs}
        return render(request, "building.html", output)
