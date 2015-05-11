# -*- coding: utf-8 -*-

from celery.task import periodic_task
from datetime import timedelta


@periodic_task(run_every=timedelta(seconds=30))
def verification():
    from my_game.function import check_all_user

    check_all_user()
    print "is works!"
