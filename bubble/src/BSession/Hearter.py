# -*- coding:utf-8 -*-

import os
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

            task = self._queue_pool.get_proc_task(self._heart_interval)
            if task is not None:
                self.hand(task)

    def hand(self,task):
        #关闭程序
        #发送监控数据

        if True:
            #防止Hearter不在主进程也能正确触发主线程的关闭
            os.kill(self._pid, signal.SIGTERM)
        pass







