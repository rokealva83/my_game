# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
import math
from my_game.models import Planet
from my_game.models import System, Asteroid_field, Flightplan_scan
from my_game.models import Fleet, Fuel_pattern, Fuel_tank
from my_game.models import Flightplan, Flightplan_flight, Fleet_parametr_scan, Flightplan_production
from my_game.models import Mail
from my_game.flightplan.start import start_flight, start_colonization, start_extraction, start_refill, \
    start_repair_build, start_scaning, start_unload_hold, start_upload_hold
from my_game.flightplan.veryfication.flight_verification import verification_flight
from my_game.flightplan.veryfication.scan_veryfication import scan_veryfication
from my_game.flightplan import fuel

def extraction_veryfication(*args):
    a=1
