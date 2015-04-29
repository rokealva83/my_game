# -*- coding: utf-8 -*-

from django.contrib import admin
from my_game.models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    search_fields = ['user_name', 'premium_account']
    list_display = ['user_name', 'internal_currency', 'foreigh_currency', 'real_currency', 'e_mail', 'premium_account', 'time_left_premium']

admin.site.register(MyUser, MyUserAdmin)



# admin.site.register(Galaxy)
# admin.site.register(System)
# admin.site.register(Planet)
# admin.site.register(Warehouse)
# admin.site.register(User_city)
# admin.site.register(Race)
# admin.site.register(User_scientic)
# admin.site.register(Basic_scientic)
# admin.site.register(Basic_armor)
# admin.site.register(Basic_engine)
# admin.site.register(Basic_factory)
# admin.site.register(Basic_generator)
# admin.site.register(Basic_hull)
# admin.site.register(Basic_module)
# admin.site.register(Basic_shield)
# admin.site.register(Basic_shell)
# admin.site.register(Basic_weapon)
# admin.site.register(Turn_scientic)

