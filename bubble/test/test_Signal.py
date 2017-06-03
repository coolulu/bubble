# -*- coding:utf-8 -*-

#linux有效
import os
import signal
from time import sleep


def onsignal_term(sig, action):
    print 'onsignal_term\n'


# 这里是绑定信号处理函数，将SIGTERM绑定在函数onsignal_term上面
signal.signal(signal.SIGTERM, onsignal_term)

while 1:
    pid = os.getpid()
    print 'pid = ', pid
    os.kill(pid, signal.SIGTERM)
    sleep(10)