# -*- coding: utf-8 -*-

from celery.task import task
from celery.task import periodic_task
from datetime import timedelta

@periodic_task(run_every=timedelta(seconds=60))
def test():
    from my_game.function import check_all_queues
    check_all_queues(2)
    print "is works!"


@task
def test2():
    print "BIG FUNNY"