# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse
from my_game.models import WarehouseComplex
from my_game import function
from my_game.building.create_complex_output import create_complex_output


def complex_warehouse(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        complex_id = request.POST.get('complex_id')
        warehouse_resource = request.POST.get('warehouse_resource')
        resource_amount = request.POST.get('resource_amount')
        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                             id_resource=warehouse_resource).first()
        if warehouse is not None and int(warehouse.amount) >= int(resource_amount):
            new_amount = int(warehouse.amount) - int(resource_amount)
            Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                     id_resource=warehouse_resource).update(amount=new_amount)
            warehouse_complex = WarehouseComplex.objects.filter(complex_id=complex_id,
                                                                id_resource=warehouse_resource).first()
            if warehouse_complex:
                new_amount = int(warehouse_complex.amount) + int(resource_amount)
                WarehouseComplex.objects.filter(complex_id=complex_id, id_resource=warehouse_resource).update(
                    amount=new_amount)
            else:
                warehouse_complex = WarehouseComplex(
                    complex_id=complex_id,
                    id_resource=warehouse_resource,
                    amount=int(resource_amount)
                )
                warehouse_complex.save()
            message = 'Ресурсы переданы комплексу'
        else:
            message = 'Нехватает ресурсов на основном складе'

        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = create_complex_output(session_user, session_user_city, complex_id, message)
        return render(request, "building.html", output)
