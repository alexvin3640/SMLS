"""Обработчик заявок rabbitmq с выдачей результата в БД"""

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
import hashlib
import pika
import redis
from solver.model import *
import argparse


def _callback(ch, method, properties, body):
    """Получает на вход изображение, выдает ответ в redis"""
    file = io.BytesIO(body)
    data = file.read()
    fn = int(hashlib.sha1(data).hexdigest(), 16)
    if args.l:
        print("Принят ", fn)
    try:
        x = steg_search(data, fn)
        x = x[0][1]
    except:
        x = 0
    if x > 0.5:
        answer = 'Есть стеганография'
    else:
        answer = 'Нет стеганографии'
    r.set(fn, answer)
    r.expire(fn, 600)
    if args.l:
        print("Готово")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ != "__main__":
    raise Exception("Run worker.consumer, don't import!")
else:
    parser = argparse.ArgumentParser(add_help=True, description='Обработчик заявок rabbitmq с выдачей результата в БД')
    parser.add_argument('--version', action='version', version='%(prog)s 0.95', help='Показать версию')
    parser.add_argument('-l', dest='l', action='store_true', default=False, help='Вывод логов загрузки')
    args = parser.parse_args()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters())
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print('\n*** Waiting for messages. To exit press CTRL+C')

    channel.basic_qos()
    channel.basic_consume(queue='task_queue', on_message_callback=_callback)
    r = redis.StrictRedis()
    channel.start_consuming()
