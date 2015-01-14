from django.contrib import admin
from my_game.models import MyUser
from my_game.models import Planet
from my_game.models import Galaxy
from my_game.models import System
from my_game.models import Warehouse
from my_game.models import User_city
from my_game.models import Race
from my_game.models import Basic_scientic
from my_game.models import Basic_armor
from my_game.models import Basic_engine
from my_game.models import Basic_factory
from my_game.models import Basic_generator
from my_game.models import Basic_hull
from my_game.models import Basic_module
from my_game.models import Basic_shell
from my_game.models import Basic_shield
from my_game.models import Basic_weapon
from  my_game.models import User_scientic
from  my_game.models import Turn_scientic


class UserAdmin(admin.ModelAdmin):
    list_filter = ['time_registration']


admin.site.register(MyUser)
admin.site.register(Galaxy)
admin.site.register(System)
admin.site.register(Planet)
admin.site.register(Warehouse)
admin.site.register(User_city)
admin.site.register(Race)
admin.site.register(User_scientic)
admin.site.register(Basic_scientic)
admin.site.register(Basic_armor)
admin.site.register(Basic_engine)
admin.site.register(Basic_factory)
admin.site.register(Basic_generator)
admin.site.register(Basic_hull)
admin.site.register(Basic_module)
admin.site.register(Basic_shield)
admin.site.register(Basic_shell)
admin.site.register(Basic_weapon)
admin.site.register(Turn_scientic)