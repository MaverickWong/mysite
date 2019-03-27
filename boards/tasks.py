from __future__ import absolute_import
from celery import shared_task

@shared_task
def add(x, y):
    print('task working')
    return x + y



# from celery import Celery
#
# app = Celery('tasks', broker='amqp://localhost')
# @app.task
# def add(x, y):
#    print('task working')
#    return x + y