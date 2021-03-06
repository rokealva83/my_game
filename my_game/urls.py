from django.conf.urls import patterns, include, url
from django.contrib import admin

from my_game.account import views as account
from my_game.account.registration import add_user
from my_game.account.user_auth import user_auth

from my_game.knowledge import views as knowledge

from my_game.civilization import views as civilization

from my_game.warehouse import views as warehouse

from my_game.administrator import views as administration
from my_game.administrator.asteroid_generation import asteroid_generation
from my_game.administrator.star_generation import star_generation

from my_game.building.views import building
from my_game.building.choice_build import choice_build
from my_game.building.working import working
from my_game.building.create_complex import create_complex
from my_game.building.management_complex import management_complex
from my_game.building.add_in_complex import add_in_complex
from my_game.building.complex_warehouse import complex_warehouse
from my_game.building.percent_extraction import percent_extraction
from my_game.building.remove_from_complex import remove_from_complex

from my_game.factory import views as factory
from my_game.factory import produce_warehouse as produce_warehouse
from my_game.factory import complex_production as complex_production
from my_game.factory import choice_complex as choice_complex
from my_game.factory import choice_element as choice_element
from my_game.factory import production as production

from my_game.designing_ships import views as design_views
from my_game.designing_ships import new_ship as new_ship
from my_game.designing_ships import work_with_project as work_with_project

from my_game.space_forces import work_with_ship as modificate_ship
from my_game.space_forces.action_modificate_ship import action_modificate_ship
from my_game.space_forces.choise_project import choise_project
from my_game.space_forces import views as space_forces
from my_game.space_forces.fleet_flightplan import fleet_flightplan
from my_game.space_forces.fleet_management import fleet_manage
from my_game.space_forces.delete_ship import delete_ship
from my_game.space_forces.add_ship import add_ship
from my_game.space_forces.start_flight import start_flightplan
from my_game.space_forces.fleet_hold import fleet_hold
from my_game.space_forces.hold_and_tank.empty_fleet_hold import empty_fleet_hold
from my_game.space_forces.fuel_tank import fuel_tank
from my_game.space_forces.hold_and_tank.empty_fuel_tank import empty_fuel_tank

from my_game.trade import views as trade
from my_game.trade.new_trade_space import new_trade_space
from my_game.trade import add_trade_element as add_trade_element
from my_game.trade import del_trade_element as del_trade_element
from my_game.trade import buy_trade_element as buy_trade_element
from my_game.trade import create_trade_fleet as create_trade_fleet
from my_game.trade import buy_credit as buy_credit
from my_game.trade import delivery as delivery

from my_game.diplomacy import views as diplomacy
from my_game.diplomacy import send_mail as send_mail
from my_game.diplomacy import remove_mail as remove

from my_game.chat import views as chatroom
from my_game.chat import private_message as private_chatroom

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^index/', 'my_game.views.home'),
                       url(r'^$', 'my_game.views.home', name='home'),

                       url(r'^registration.html', account.registration, name='account.registration'),
                       url(r'^index.html', add_user, name='account.add_user'),
                       url(r'^auth', user_auth, name='account.auth'),

                       url(r'^admin/administration', administration.administration),
                       url(r'^admin/generation', administration.generation),
                       url(r'^admin/star_generation', star_generation),
                       url(r'^admin/asteroid_generation', asteroid_generation),

                       url(r'^civilization', civilization.civilization),

                       url(r'^warehouse', warehouse.warehouse),

                       url(r'^knowledge', knowledge.knowledge),
                       url(r'^study', knowledge.study),

                       url(r'^building', building),
                       url(r'^choice_build', choice_build),
                       url(r'^create_complex', create_complex),
                       url(r'^management_complex', management_complex),
                       url(r'^add_in_complex', add_in_complex),
                       url(r'^percent_extraction', percent_extraction),
                       url(r'^remove_from_complex', remove_from_complex),
                       url(r'^complex_warehouse', complex_warehouse),
                       url(r'^working', working),

                       url(r'^factory', factory.factory),
                       url(r'^choice_element', choice_element.choice_element),
                       url(r'^choice_complex', choice_complex.choice_complex),
                       url(r'^production', production.production),
                       url(r'^complex_production', complex_production.complex_production),
                       url(r'^produce_warehouse', produce_warehouse.produce_warehouse),

                       url(r'^designingships', design_views.designingships),
                       url(r'^new_ship', new_ship.new_ship),
                       url(r'^modificate_ship', modificate_ship.modificate_ship),
                       url(r'^choise_project', choise_project),
                       url(r'^action_modificate_ship', action_modificate_ship),
                       url(r'^work_with_project', work_with_project.work_with_project),

                       url(r'^space_forces', space_forces.space_forces),
                       url(r'^fleet_manage', fleet_manage),
                       url(r'^delete_ship', delete_ship),
                       url(r'^add_ship', add_ship),
                       url(r'^fleet_flightplan', fleet_flightplan),
                       url(r'^start_flight', start_flightplan),
                       url(r'^fleet_hold', fleet_hold),
                       url(r'^empty_fleet_hold', empty_fleet_hold),
                       url(r'^fuel_tank', fuel_tank),
                       url(r'^unload_fuel', empty_fuel_tank),
                       url(r'^unload_fuel_all', empty_fuel_tank),

                       url(r'^trade', trade.trade),
                       url(r'^new_trade_space', new_trade_space),
                       url(r'^add_trade_element', add_trade_element.add_trade_element),
                       url(r'^del_trade', del_trade_element.del_trade),
                       url(r'^buy_trade', buy_trade_element.buy_trade),
                       url(r'^create_trade_fleet', create_trade_fleet.create_trade_fleet),
                       url(r'^buy_credit', buy_credit.buy_credit),
                       url(r'^delivery', delivery.delivery),

                       url(r'^diplomacy', diplomacy.diplomacy),
                       url(r'^send_mail', send_mail.send_mail),
                       url(r'^remove', remove.remove_mail),
                       url(r'^remove_all', remove.remove_mail),

                       url(r'^chat', chatroom.chat),
                       url(r'^send_message', chatroom.send_message),
                       url(r'^update_message', chatroom.update_message),
                       url(r'^user_delete', chatroom.user_delete),
                       url(r'^update_user', chatroom.update_user),
                       url(r'^delete_user_update', chatroom.delete_user_update),
                       url(r'^send_private_message', private_chatroom.send_private_message),
                       url(r'^update_private_message', private_chatroom.update_private_message),
                       )
