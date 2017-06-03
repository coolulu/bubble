# -*- coding:utf-8 -*-

from bubble.config import BSessionCfg
from Public import init_mq
from Distributer import Distributer

class Recver:

    def __init__(self, queue_pool):
        self._distributer = Distributer(queue_pool)

    def recving(self):
        mq = init_mq()
        mq.declare(BSessionCfg.mq_recv_queue, self.recv_cb)
        mq.recv_msg()

    def recv_cb(self, ch, method, properties, body):
        self._distributer.distributing(body)
