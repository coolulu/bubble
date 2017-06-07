# -*- coding:utf-8 -*-

from bubble.config import BSessionCfg
from bubble.common.mq.RabbitMQClient import RabbitMQClient
from Distributer import Distributer
from datetime import datetime

class Recver:

    def __init__(self, queue_pool, recv_queue):
        self._distributer = Distributer(queue_pool)
        self._recv_queue = recv_queue

    def recving(self):
        mq = RabbitMQClient.init_mq(BSessionCfg.MQ.user_name,
                                    BSessionCfg.MQ.password,
                                    BSessionCfg.MQ.host,
                                    BSessionCfg.MQ.port,
                                    BSessionCfg.MQ.virtual_host)
        mq.declare(self._recv_queue, self.recv_cb)
        mq.recv_msg()

    def recv_cb(self, ch, method, properties, body):
        print 'recv: %s' % datetime.now()
        self._distributer.distributing(body)
