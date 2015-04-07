# -*- coding: utf-8 -*-

import math
import random
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User

from my_game.models import Galaxy, System, Planet, MyUser, User_city, Warehouse, Turn_production, Turn_building, \
    Turn_assembly_pieces
from my_game.models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Factory_installed
from my_game.models import Warehouse_factory, Warehouse_element
import function
import verification_func
from my_game.models import Project_ship, Element_ship, Turn_ship_build, Ship, Fleet, Race, Mail


def send_mail(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)

        target = request.POST.get('message_target')
        target_name = MyUser.objects.filter(user_name=target).first()
        if target_name is None:
            message = 'GGGGGGGGGGGGGGGGGGGGgg'
        else:
            title = request.POST.get('title')
            mail = request.POST.get('message')
            user = MyUser.objects.filter(user_id=session_user).first()
            user_name = user.user_name

            new_mail = Mail(
                user=target_name.user_id,
                recipient=session_user,
                time=datetime.now(),
                status=1,
                category=1,
                login_recipient=user_name,
                title=title,
                message=mail
            )
            new_mail.save()

        mails = Mail.objects.filter(user=session_user).order_by('category', '-time')
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user = MyUser.objects.filter(user_id=session_user).first()
        user_city = User_city.objects.filter(user=int(session_user)).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'mails': mails}
        return render(request, "diplomacy.html", output)