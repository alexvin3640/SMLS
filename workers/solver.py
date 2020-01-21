"""Создание таска для rabbitmq"""

__author__ = 'alexander'
__maintainer__ = 'alexander'
__credits__ = ['alexander', ]
__copyright__ = "LGPL"
__status__ = 'Development'
__version__ = '20200121'

import os
import sys
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_PATH)
# ! --------------------------
import pika


def produce(path, filename, fn) -> None:
    """
    Сохранение загруженного файла и передача в rabbitmq
    :param path: путь к файлу
    :param filename: имя файла
    :param fn: хэш файла
    """
    file = open('{}/{}'.format(path, filename), 'rb')
    data = file.read()
    file.close()
    os.remove('{}/{}'.format(path, filename))
#   print(type(file))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters())
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    message = data
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        )
#   print(" [x] Sent %r" % fn)
