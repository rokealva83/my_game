# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Shell_pattern, Factory_pattern
from my_game.models import Warehouse_element, Warehouse_factory
from my_game import function
from my_game.models import Project_ship, Ship
from my_game.models import Trade_element, Trade_space


def buy_trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)

        full_request = request.POST
        myDict = dict(full_request.iterlists())
        trade_space_id = myDict.get('trade_space_id')
        trade_space_id = int(trade_space_id[0])
        id_element = myDict.get('trade_buy')
        id_element = int(id_element[0])
        amount = myDict.get('amount')
        amount = int(amount[0])
        set_aside = myDict.get('set_aside')
        method = myDict.get('method')
        method = int(method[0])

        trade_element = Trade_element.objects.filter(id = id_element).first()
        price_element = trade_element.amount/trade_element.cost * amount
        user = MyUser.objects.filter(user_id = session_user).first()
        if user.foreigh_currency >= price_element:
            r = 2

