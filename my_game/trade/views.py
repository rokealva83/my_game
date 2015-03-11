# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern
from my_game.models import Warehouse_element
from my_game import function
from my_game.models import Project_ship, Element_ship, Turn_ship_build
from my_game.models import Trade_element, Trade_space


def trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        message = ''
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        trade_spaces = Trade_space.objects.filter()

        trade_space_id = request.POST.get('trade_space_id')
        if trade_space_id is not None:
            password = request.POST.get('password')
            trade_space = Trade_space.objects.filter(id = trade_space_id).first()
            trade_pass = trade_space.password
            if password == trade_space.password:
                message = 'Правильный пароль'
            else:
                message = 'Неправильный пароль'

            request.session['userid'] = session_user
            request.session['user_city'] = session_user_city
            request.session['live'] = True
            output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                      'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id, 'message': message}
            return render(request, "trade.html", output)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id}
        return render(request, "trade.html", output)


def new_trade_space(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        trade_space_id = request.POST.get('trade_space_id')
        name = request.POST.get('name')
        password = request.POST.get('pass')
        tax = request.POST.get('tax')
        trade_space = Trade_space(
            name=name,
            user=session_user,
            password=password,
            tax=tax
        )
        trade_space.save()
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        trade_spaces = Trade_space.objects.filter()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id}
        return render(request, "trade.html", output)

