# -*- coding:utf-8 -*-

from Public import init_mq

class Sender:

    def __init__(self, queue_pool):
        self._queue_pool = queue_pool

    def sending(self):
        mq = init_mq()
        while True:
            msg = self._queue_pool.get_send_task()
            mq.send_msg(msg, msg)