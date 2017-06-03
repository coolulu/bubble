# -*- coding:utf-8 -*-


class Worker:

    def __init__(self, index, queue_pool):
        self._index = index
        self._queue_pool = queue_pool

    def working(self):
        while True:
            msg = self._queue_pool.get_work_task(self._index)
            self._queue_pool.put_send_task(msg)

