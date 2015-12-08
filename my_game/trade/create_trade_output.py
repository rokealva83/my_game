# -*- coding: utf-8 -*-

from my_game.models import MyUser, UserCity
from my_game.models import HullPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, ShellPattern, FactoryPattern, DevicePattern
from my_game.models import WarehouseElement, WarehouseFactory, BasicResource
from my_game.models import ProjectShip, Ship
from my_game.models import TradeElement, TradeSpace, BuildingInstalled, DeliveryQueue


def create_trade_output(session_user, session_user_city, output, trade_space_id, message):
    warehouse = session_user_city.warehouse
    basic_resources = BasicResource.objects.all()
    user_citys = UserCity.objects.filter(user=session_user).all()
    warehouse_elements = WarehouseElement.objects.filter(user=session_user,
                                                         user_city=session_user_city).order_by('element_class',
                                                                                               'element_id')
    warehouse_factorys = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city).all()
    factory_patterns = FactoryPattern.objects.filter(user=session_user).all()
    hull_patterns = HullPattern.objects.filter(user=session_user).all()
    armor_patterns = ArmorPattern.objects.filter(user=session_user).all()
    shield_patterns = ShieldPattern.objects.filter(user=session_user).all()
    engine_patterns = EnginePattern.objects.filter(user=session_user).all()
    generator_patterns = GeneratorPattern.objects.filter(user=session_user).all()
    weapon_patterns = WeaponPattern.objects.filter(user=session_user).all()
    shell_patterns = ShellPattern.objects.filter(user=session_user).all()
    module_patterns = ModulePattern.objects.filter(user=session_user).all()
    device_patterns = DevicePattern.objects.filter(user=session_user).all()
    trade_building = BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                      production_class=21).first()
    delivery_queues = DeliveryQueue.objects.filter(user=session_user, user_city=session_user_city.id).all()
    ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
    project_ships = ProjectShip.objects.filter(user=session_user).all()
    users = MyUser.objects.all()
    user_trade_elements = TradeElement.objects.filter(trade_space=trade_space_id, user=session_user)
    trade_elements = TradeElement.objects.filter(trade_space=trade_space_id)
    trade_spaces = TradeSpace.objects.filter()
    trade_space = TradeSpace.objects.filter(id=trade_space_id).first()

    output.update({'user': session_user, 'warehouse': warehouse, 'user_city': session_user_city, 'user_citys': user_citys,
              'basic_resources': basic_resources, 'warehouse_factorys': warehouse_factorys,
              'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
              'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
              'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
              'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns, 'device_patterns': device_patterns,
              'module_patterns': module_patterns, 'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id,
              'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements, 'users': users,
              'user_trade_elements': user_trade_elements, 'trade_space': trade_space, 'message': message,
              'trade_building': trade_building, 'delivery_queues': delivery_queues})
    return output
