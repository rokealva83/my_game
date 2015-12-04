# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import ManufacturingComplex, WarehouseComplex
from my_game import function
from my_game.building.create_complex_output import create_complex_output


def create_complex(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        warehouse_complex = WarehouseComplex()
        warehouse_complex.save()
        name = request.POST.get('complex_name')
        manufacturing_complex = ManufacturingComplex(
            user=session_user,
            user_city=session_user_city,
            name=name,
            warehouse_complex=warehouse_complex
        )
        manufacturing_complex.save()
        message = 'Комплекс создано'
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = create_complex_output(session_user, session_user_city, manufacturing_complex, message)
        return render(request, "building.html", output)
