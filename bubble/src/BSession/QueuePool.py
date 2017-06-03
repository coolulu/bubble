# -*- coding:utf-8 -*-

import multiprocessing

class QueuePool:
    '''
    [0, work_num]   为工作进程队列
    [work_num]/[-2] 为程序控制队列
    [work_num]/[-1] 为发送队列
    '''

    def __init__(self, work_num):
        self._work_num = work_num
        self._queues = [multiprocessing.Queue()] * (self._work_num + 2)

    '''
    工作进程队列操作
    '''
    def put_work_task(self, index, task):
        self._queues[index].put(task)

    def get_work_task(self, index):
        return self._queues[index].get()

    def get_work_size(self, index):
        return self._queues[index].qsize()

    def get_work_index(self, index):
        return index % self._work_num

    '''
    发送进程队列操作
    '''
    def put_send_task(self, task):
        self._queues[-1].put(task)

    def get_send_task(self):
        return self._queues[-1].get()

    def get_send_size(self):
        return self._queues[-1].qsize()

    '''
    程序控制队列操作
    '''
    def put_proc_task(self, task):
        self._queues[-2].put(task)

    def get_proc_task(self, interval):
        try:
            return self._queues[-2].get(timeout=interval)
        except:
            return None

def test():
    num = 10
    ql = QueuePool(num)
    for i in range(num):
        print ql.get_work_size(ql.get_work_index(i))
    print ql.get_send_size()

    print ql.get_proc_task(5)

test()
