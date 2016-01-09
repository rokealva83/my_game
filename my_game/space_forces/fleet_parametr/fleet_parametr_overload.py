from my_game.models import FleetOverload


def fleet_parametr_overload(*args):
    fleet = args[0]
    ship_overload_elements = args[1]
    ship_amount = args[2]
    overload = 0
    for ship_overload_element in ship_overload_elements:
        overload += ship_overload_element.param1
    overloads = overload * ship_amount * args[3]
    if overloads:
        fleet_overload = FleetOverload.objects.filter(fleet=fleet).first()
        if fleet_overload:
            new_overload = fleet_overload.overload + overloads
            setattr(fleet_overload, 'overload', new_overload)
            fleet_overload.save()
        else:
            fleet_overload = FleetOverload(
                fleet=fleet,
                overload=overloads
            )
            fleet_overload.save()
    return True
