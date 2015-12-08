# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game import function
from my_game.trade.create_trade_output import create_trade_output


def buy_credit(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        message = ''
        trade_space_id = request.POST.get('trade_space_id')
        user = MyUser.objects.filter(user_id=session_user).first()
        foreigh_currency = user.foreigh_currency
        internal_currency = user.internal_currency
        amount_foreigh = int(request.POST.get('amount'))
        operation = int(request.POST.get('operation'))
        if operation == 0:
            need_internal_currency = amount_foreigh * 500
            if internal_currency >= need_internal_currency:
                new_internal_currency = internal_currency - need_internal_currency
                new_foreigh_currency = foreigh_currency + amount_foreigh
                MyUser.objects.filter(user_id=session_user).update(internal_currency=new_internal_currency,
                                                                   foreigh_currency=new_foreigh_currency)
                message = 'Покупка совершена'
            else:
                message = 'Нехватка внутренней валюты'
        else:
            if foreigh_currency >= amount_foreigh:
                bought_currency = amount_foreigh * 495
                new_internal_currency = internal_currency + bought_currency
                new_foreigh_currency = foreigh_currency - amount_foreigh
                MyUser.objects.filter(user_id=session_user).update(internal_currency=new_internal_currency,
                                                                   foreigh_currency=new_foreigh_currency)
                message = 'Продажа совершена'
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True

        output = create_trade_output(session_user, session_user_city, output, trade_space_id, message)
        return render(request, "trade.html", output)
