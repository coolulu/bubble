# -*- coding:utf-8 -*-

from Public import init_mq
from datetime import datetime

class Sender:

    def __init__(self, queue_pool, loop_back_queue):
        self._queue_pool = queue_pool
        self._loop_back_queue = loop_back_queue

    def sending(self):
        mq = init_mq()
        while True:
            msg = self._queue_pool.get_send_task()
            queue_name = msg
            print 'send: %s' % datetime.now()

            #防止自发自收
            if queue_name != self._loop_back_queue:
                mq.send_msg(queue_name, msg)