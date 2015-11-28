# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import ManufacturingComplex
from my_game import function, verification_func
from my_game.building.create_complex_output import create_complex_output


def percent_extraction(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        verification_func.verification_of_resources(session_user)
        complex_id = request.POST.get('complex_id')
        new_percent = request.POST.get('percent_extraction')
        ManufacturingComplex.objects.filter(id=complex_id).update(extraction_parametr=new_percent)
        message = ''
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = create_complex_output(session_user, session_user_city, complex_id, message)
        return render(request, "building.html", output)
