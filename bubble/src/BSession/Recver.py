# -*- coding:utf-8 -*-

from bubble.config import BSessionCfg
from bubble.common.mq.RabbitMQClient import RabbitMQClient
from Distributer import Distributer
from datetime import datetime

class Recver:

    def __init__(self, queue_pool, mq_recv_queue):
        self._distributer = Distributer(queue_pool)
        self._mq_recv_queue = mq_recv_queue

    def recving(self):
        mq = RabbitMQClient.init_mq(BSessionCfg.mq_user_name,
                                    BSessionCfg.mq_password,
                                    BSessionCfg.mq_host,
                                    BSessionCfg.mq_port,
                                    BSessionCfg.mq_virtual_host)
        mq.declare(self._mq_recv_queue, self.recv_cb)
        mq.recv_msg()

    def recv_cb(self, ch, method, properties, body):
        print 'recv: %s' % datetime.now()
        self._distributer.distributing(body)
