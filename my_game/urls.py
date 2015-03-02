from django.conf.urls import patterns, include, url
from django.contrib import admin
from my_game.account import views as account
from my_game.knowledge import views as knowledge
from my_game.civilization import views as civilization
from my_game.warehouse import views as warehouse
from my_game.administrator import views as administration
from my_game.building import views as building
from my_game.factory import views as factory
from my_game.designing_ships import views as design_views
from my_game.designing_ships import new_ship as new_ship
from my_game.designing_ships import work_with_project as work_with_project

# import my_game.registration.registration

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'my_game.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^index/', 'my_game.views.home'),
                       url(r'^$', 'my_game.views.home', name='home'),

                       url(r'^registration.html', account.registration, name='account.registration'),
                       url(r'^index.html', account.add_user, name='account.add_user'),
                       url(r'^auth', account.auth, name='account.auth'),

                       url(r'^admin/administration', administration.administration),
                       url(r'^admin/generation', administration.generation),
                       url(r'^admin/star_generation', administration.star_generation),

                       url(r'^civilization', civilization.civilization),
                       url(r'^warehouse', warehouse.warehouse),

                       url(r'^knowledge', knowledge.knowledge),
                       url(r'^study', knowledge.study),

                       url(r'^building', building.building),
                       url(r'^choice_build', building.choice_build),
                       url(r'^working', building.working),


                       url(r'^factory', factory.factory),
                       url(r'^choice_element', factory.choice_element),
                       url(r'^production', factory.production),

                       url(r'^designingships', design_views.designingships),
                       url(r'^new_ship', new_ship.new_ship),
                       url(r'^work_with_project', work_with_project.work_with_project),

                       url(r'space_forces', 'my_game.views.space_forces', name='space_forces'),
                       url(r'fleet_manage', 'my_game.fleet_management.fleet_manage', name='fleet_manage'),
                       url(r'trade', 'my_game.views.trade', name='trade'),
                       url(r'fleet_fly', 'my_game.fleet_management.fleet_fly', name='fleet_fly'),
                       url(r'start_flight', 'my_game.fleet_management.start_flight', name='start_flight'),

)
