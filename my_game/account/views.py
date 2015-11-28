# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import Race


def registration(request):
    races = Race.objects.all()
    return render(request, "registration.html", {'races': races})
