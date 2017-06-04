# -*- coding:utf-8 -*-

#linux有效
import os
import signal
from time import sleep

def f1(sig, action):
    print 'f1'

def f2(sig, action):
    print 'f2'

signal.signal(signal.SIGUSR1, f1) #BGATE 主进程统计 连接加1
signal.signal(signal.SIGUSR2, f2) #BGATE 主进程统计 连接减1

while 1:
    pid = os.getpid()
    print 'pid = ', pid
    os.kill(pid, signal.SIGUSR1)
    os.kill(pid, signal.SIGUSR2)
    sleep(10)
