# -*- coding:utf-8 -*-

import multiprocessing
import os
import signal

from bubble.config import BSessionCfg

from bubble.common.log.log import log, logger
from QueuePool import QueuePool
from Hearter import Hearter
from Sender import Sender
from Recver import Recver
from Worker import Worker



g_opened = True

def signal_close(sig, action):
    global g_opened
    g_opened = False

def proc_close(queue_pool):
    pass

def main():
    signal.signal(signal.SIGINT, signal_close)
    signal.signal(signal.SIGTERM, signal_close)

    log = logger(BSessionCfg.Log.level,
                 BSessionCfg.Log.module,
                 BSessionCfg.Log.path,
                 BSessionCfg.Log.maxsize)
    queue_pool = QueuePool(BSessionCfg.Proc.work_num)

    procList = []
    for index in range(BSessionCfg.Proc.work_num):
        procList.append(multiprocessing.Process(target=Worker.working,
                                                args=(Worker(index, queue_pool),)))
    procList.append(multiprocessing.Process(target=Sender.sending,
                                            args=(Sender(queue_pool, BSessionCfg.MQ.recv_queue),)))
    procList.append(multiprocessing.Process(target=Recver.recving,
                                            args=(Recver(queue_pool, BSessionCfg.MQ.recv_queue),)))

    for proc in procList:
        proc.start()

    global g_opened
    hearter = Hearter(os.getpid(),
                      g_opened,
                      BSessionCfg.Proc.heart_interval,
                      queue_pool)
    hearter.hearting()

    proc_close(queue_pool)

    for proc in procList:
        proc.join()

if __name__ in '__main__':
    main()