from __future__ import absolute_import
from celery import shared_task

from tasklist.models import Task


@shared_task
def add(x, y):
    print('task working')
    t = Task.objects.create(name='new')
    # t.save()
    return '\n result is ' + str(x + y)



# from celery import Celery
#
# app = Celery('tasks', broker='amqp://localhost')
# @app.task
# def add(x, y):
#    print('task working')
#    return x + y