# -*- coding:utf-8 -*-

from Handle.HandleBase import HandleBase

class Worker:

    def __init__(self, index, queue_pool):
        self._index = index
        self._queue_pool = queue_pool

    def working(self):
        while True:
            msg = self._queue_pool.get_work_task(self._index)
            if msg is None:
                break
            else:
                h = HandleBase()
                msg = h.handle(msg)
                if msg is not None:
                    self._queue_pool.put_send_task(msg)

