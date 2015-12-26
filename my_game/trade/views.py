# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game import function
from my_game.models import TradeSpace, BuildingInstalled
from my_game.trade.create_trade_output import create_trade_output


def trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        trade_building = BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                          production_class=21).first()
        if trade_building:
            trade_space_id = 1

            trade_id = request.POST.get('trade_space_id')
            message = ''
            if trade_id is not None:
                password = request.POST.get('password')
                trade_space = TradeSpace.objects.filter(id=trade_id).first()
                if password == trade_space.password:
                    trade_space_id = trade_id
                request.session['user'] = session_user.id
                request.session['user_city'] = session_user_city.id
                request.session['live'] = True
                output = create_trade_output(session_user, session_user_city, trade_space_id, message)
                return render(request, "trade.html", output)

            request.session['user'] = session_user.id
            request.session['user_city'] = session_user_city.id
            request.session['live'] = True
            output = create_trade_output(session_user, session_user_city, trade_space_id, message)
            return render(request, "trade.html", output)
        else:
            warehouse = session_user_city.warehouse
            user_citys = UserCity.objects.filter(user=session_user)
            planet = session_user_city.planet
            request.session['user'] = session_user.id
            request.session['user_city'] = session_user_city.id
            request.session['live'] = True
            output = {'user': session_user, 'warehouse': warehouse, 'user_city': session_user_city,
                      'user_citys': user_citys, 'planet': planet}
            return render(request, "civilization.html", output)


def new_trade_space(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        message = ''
        trade_space_id = request.POST.get('trade_space_id')
        name = request.POST.get('name')
        password = request.POST.get('pass')
        tax = request.POST.get('tax')
        trade_space = TradeSpace(
            name=name,
            user=session_user,
            password=password,
            tax=tax
        )
        trade_space.save()

        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = create_trade_output(session_user, session_user_city, trade_space_id, message)
        return render(request, "trade.html", output)
