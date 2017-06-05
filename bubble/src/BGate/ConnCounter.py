# -*- coding:utf-8 -*-

import os
import signal

class ConnCounter:

    s_connCounter = None

    def __init__(self):
        self._count = 0
        self._ppid = os.getpid()
        signal.signal(signal.SIGUSR1, self.add)  # BGATE 主进程统计连接数 加1
        signal.signal(signal.SIGUSR2, self.sub)  # BGATE 主进程统计连接数 减1

        ConnCounter.s_connCounter = self

    @staticmethod
    def instance():
        return ConnCounter.s_connCounter

    def count(self):
        return self._count

    def add(self, sig, action):
        self._count += 1

    def sub(self, sig, action):
        self._count -= 1


    def kill_ppid_add(self):
        os.kill(self._ppid, signal.SIGUSR1)     #通知父进程连接数 加1

    def kill_ppid_sub(self):
        os.kill(self._ppid, signal.SIGUSR2)     #通知父进程连接数 减1


def test():

    ConnCounter()
    ConnCounter.instance().kill_ppid_add()
    ConnCounter.instance().kill_ppid_add()
    print ConnCounter.instance().count()
    ConnCounter.instance().kill_ppid_sub()
    ConnCounter.instance().kill_ppid_sub()
    print ConnCounter.instance().count()


test()