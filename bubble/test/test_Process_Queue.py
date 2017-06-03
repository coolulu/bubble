# -*- coding:utf-8 -*-

from multiprocessing import Process, Queue, Pool
import os, time, random
import datetime

# 写数据进程执行的代码:
def write(q):
    for value in range(10000):
        # print str(datetime.datetime.now()) + ' ' + str(value)
         q.put(value)

# 读数据进程执行的代码:
def read(q):
    i = 0
    while True:
        value = q.get(True)
        # print str(datetime.datetime.now()) + ' Get %s from queue.' % value
        i += 1
        print i

class Recver:
    def recv(self, q):
        print 'sss'
        pass

if __name__ == '__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()

    pw0 = Process(target=write, args=(q,))

    r = Recver()
    pw1 = Process(target=Recver.recv, args=(r, q))

    pr = Process(target=read, args=(q, ))
    pr.start()

    # write(q)
    pw0.start()
    pw1.start()

    write(q)

    pw0.join()
    pw1.join()

    pr.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    print
    print '所有数据都写入并且读完'

