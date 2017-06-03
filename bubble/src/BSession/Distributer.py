# -*- coding:utf-8 -*-

class Distributer:

    def __init__(self, queue_pool):
        self._queue_pool = queue_pool

    '''
    消息分发给队列
    '''
    def distributing(self, body):
        print self._queue_pool.get_send_size()
        print body