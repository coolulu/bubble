# -*- coding:utf-8 -*-

import pika

class RabbitMQClient:

    def __init__(self, user_name, password, host, port, virtual_host):
        self._user_name = user_name
        self._password = password
        self._host = host
        self._port = port
        self._virtual_host = virtual_host
        self._connection = None
        self._channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self._user_name, self._password)
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(self._host,
                                                                             self._port,
                                                                             self._virtual_host,
                                                                             credentials))
        self._channel = self._connection.channel()

    def close(self):
        self._connection.close()

    @staticmethod
    def init_mq(user_name, password, host, port, virtual_host):
        mq = RabbitMQClient(user_name, password, host, port, virtual_host)
        mq.connect()
        return mq

    '''
    1.由消费者来声明队列,如果队列没声明,生产者消息会丢失
    2.consumer_callback(channel, method, properties, body)
    '''
    def declare(self, queue_name, consumer_callback):
        self._channel.queue_declare(queue=queue_name)
        self._channel.basic_consume(consumer_callback, queue=queue_name, no_ack=True)

    '''
    recv blocking
    '''
    def recv_msg(self):
        self._channel.start_consuming()

    def send_msg(self, queue_name, body):
        self._channel.basic_publish(exchange='', routing_key=queue_name, body=body)

def a_cb(ch, method, properties, body):
    print 'A: ' + body

def b_cb(ch, method, properties, body):
    print 'B: ' + body

if __name__ == "__main__":
    queue_A = 'A'
    queue_B = 'B'
    body_A = 'AAAAAAAA'
    body_B = 'BBBBBBBB'

    mq = RabbitMQClient('admin', 'admin123', '192.168.154.130', 5672, '/')
    mq.connect()
    mq.declare(queue_A, a_cb)
    mq.declare(queue_B, b_cb)
    mq.send_msg(queue_A, body_A)
    mq.send_msg(queue_B, body_B)
    mq.recv_msg()

