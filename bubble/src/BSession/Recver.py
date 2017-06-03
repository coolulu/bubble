# -*- coding:utf-8 -*-

class Recver:

    def __init__(self, queue_pool, mq):
        self._queue_pool = queue_pool
        self._mq = mq

    def recving(self):
        self.mq.recv_msg()

