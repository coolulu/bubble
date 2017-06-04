# -*- coding:utf-8 -*-

class Distributer:

    def __init__(self, queue_pool):
        self._queue_pool = queue_pool

    '''
    消息分发给队列
    '''
    def distributing(self, body):
        self._queue_pool.put_work_task(0, body)