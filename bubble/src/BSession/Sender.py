# -*- coding:utf-8 -*-

class Sender:

    def __init__(self, queue_pool, mq):
        self._queue_pool = queue_pool
        self._mq = mq

    def sending(self):
        while True:
            msg = self._queue_pool.get_send_task()
            self._mq.send(msg, msg)