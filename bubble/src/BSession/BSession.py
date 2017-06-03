# -*- coding:utf-8 -*-

import multiprocessing
import time

from bubble.config import BSessionCfg


def heart(interval):
    while True:
        time.sleep(interval)

def worker(index):

    pass

def recv(index):

    pass

def send(index):

    pass

def main():
    work_queue = []
    for i in range(BSessionCfg.proc_work_num):
        work_queue.append(multiprocessing.Queue())
    pass
