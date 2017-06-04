# -*- coding:utf-8 -*-

from Public import init_mq
from Distributer import Distributer
from datetime import datetime

class Recver:

    def __init__(self, queue_pool, mq_recv_queue):
        self._distributer = Distributer(queue_pool)
        self._mq_recv_queue = mq_recv_queue

    def recving(self):
        mq = init_mq()
        mq.declare(self._mq_recv_queue, self.recv_cb)
        mq.recv_msg()

    def recv_cb(self, ch, method, properties, body):
        print 'recv: %s' % datetime.now()
        self._distributer.distributing(body)
