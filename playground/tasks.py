from celery import shared_task
from time import sleep


@shared_task
def notify_customer(message):
    print('sending 1000 email!!!')
    print(message)
    sleep(10)
    print('sending all messages done !!!')
