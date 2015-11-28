# -*- coding: utf-8 -*-

from django.shortcuts import render


def administration(request):
    return render(request, "admin/administation.html", {})


def generation(request):
    return render(request, "admin/generation.html", {})