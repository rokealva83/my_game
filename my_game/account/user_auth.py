# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.models import User
from my_game.models import MyUser
from my_game.models import UserCity

from my_game import function

# функция авторизации
def user_auth(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        login = request.POST.get('name')
        password = request.POST.get('pass')
        user = User.objects.filter(username=login).first()
        if user:
            if user.password == password:
                user = MyUser.objects.filter(user_id=user.id).first()
                user_city = UserCity.objects.filter(user=user).first()
                user_citys = UserCity.objects.filter(user=user)
                function.check_all_queues(user)
                output = {'user': user, 'race': user.race, 'warehouse': user_city.warehouse, 'user_city': user_city,
                          'user_citys': user_citys, 'planet': user_city.planet}
                request.session['user'] = user.id
                request.session['user_city'] = user_city.id
                request.session['live'] = True
                return render(request, "civilization.html", output)
            else:
                message = 'Неверно введено имя или пароль пользователя'
                output = {'message': message}
                return render(request, "index.html", output)
    return render(request, "index.html", {})
