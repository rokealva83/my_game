# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import FactoryInstalled
from my_game.models import TurnComplexProduction
from my_game import function
from my_game.building.create_complex_output import create_complex_output


def remove_from_complex(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        complex_id = request.POST.get('complex_id')
        installed_factory_id = request.POST.get('factory_id')
        turn_production = TurnComplexProduction.objects.filter(complex_id=complex_id,
                                                               factory_id=installed_factory_id).first()
        if turn_production:
            message = 'Исключение невозможно. Идет производство'
        else:
            FactoryInstalled.objects.filter(id=installed_factory_id).update(complex_status=0,
                                                                            complex_id=None)
            message = 'Производство добавлено в комплекс'
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = create_complex_output(session_user, session_user_city, complex_id, message)
        return render(request, "building.html", output)
