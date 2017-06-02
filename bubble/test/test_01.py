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

if __name__ == '__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()

    pw = Process(target=write, args=(q,))
    pw1 = Process(target=write, args=(q,))
    pw2 = Process(target=write, args=(q,))
    pw3 = Process(target=write, args=(q,))
    pw4 = Process(target=write, args=(q,))
    pw5 = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pr.start()

    # write(q)
    pw.start()
    pw1.start()
    pw2.start()
    pw3.start()
    pw4.start()
    pw5.start()
    write(q)

    pw.join()
    pw1.join()
    pw2.join()
    pw3.join()
    pw4.join()
    pw5.join()

    pr.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    print
    print '所有数据都写入并且读完'

