# -*- coding: utf-8 -*-


from my_game.models import UserCity, TurnBuilding, TurnAssemblyPieces
from my_game.models import FactoryInstalled, BasicResource
from my_game.models import ManufacturingComplex, WarehouseComplex


def create_complex_output(*args):
    session_user = args[0]
    session_user_city = args[1]
    complex_id = args[2]
    message = args[3]
    turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
    turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
    user_citys = UserCity.objects.filter(user=session_user)
    manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
    manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).first()
    factory_installeds = FactoryInstalled.objects.filter(user=session_user, complex_status=0)
    complex_factorys = FactoryInstalled.objects.filter(user=session_user, complex_status=1, complex_id=complex_id)
    basic_resources = BasicResource.objects.filter()
    warehouse_complexs = WarehouseComplex.objects.filter(complex_id=complex_id).order_by('resource_id')

    output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
              'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
              'user_citys': user_citys, 'message': message, 'complex_id': complex_id,
              'manufacturing_complexs': manufacturing_complexs, 'manufacturing_complex': manufacturing_complex,
              'factory_installeds': factory_installeds, 'complex_factorys': complex_factorys,
              'basic_resources': basic_resources, 'warehouse_complexs': warehouse_complexs}
    return output
