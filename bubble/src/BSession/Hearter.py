# -*- coding:utf-8 -*-

import signal

class Hearter:

    def __init__(self, pid, opened, heart_interval, queue_pool):
        self._pid = pid
        self._opened = opened
        self._heart_interval = heart_interval
        self._queue_pool = queue_pool

    def hearting(self):
        while self._opened:
            # 触发心跳
            msg = 'heart'
            self._queue_pool.put_send_task(msg)

            task = self._queue_pool.get_proc_task(msg, self._heart_interval)
            if task is not None:
                self.hand(task)

    def hand(self,task):
        #关闭程序
        #发送监控数据

        if True:
            os.kill(self._pid, signal.SIGTERM)
        pass







