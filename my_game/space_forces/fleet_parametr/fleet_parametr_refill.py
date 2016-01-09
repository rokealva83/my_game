from my_game.models import FleetFuelRefill


def fleet_parametr_refill(*args):
    fleet = args[0]
    ship_refill_elements = args[1]
    ship_amount = args[2]
    refill = 0
    for ship_refill_element in ship_refill_elements:
        refill += ship_refill_element.param1
    refills = refill * ship_amount * args[3]
    if refills:
        fleet_refill = FleetFuelRefill.objects.filter(fleet=fleet).first()
        if fleet_refill:
            new_refill = fleet_refill.fuel_refill + refills
            setattr(fleet_refill, 'fuel_refill', new_refill)
            fleet_refill.save()
        else:
            fleet_refill = FleetFuelRefill(
                fleet=fleet,
                fuel_refill=refills
            )
            fleet_refill.save()
    return True
