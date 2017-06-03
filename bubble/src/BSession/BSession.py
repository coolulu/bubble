# -*- coding:utf-8 -*-

import multiprocessing
import os
import signal

from bubble.config import BSessionCfg
from bubble.common.mq.RabbitMQClient import RabbitMQClient
from bubble.common.log.log import log, logger
from QueuePool import QueuePool, g_queue_pool
from Hearter import Hearter
from Sender import Sender
from Recver import Recver
from Worker import Worker
from Distributer import distributing


g_opened = True

def signal_close(sig, action):
    global g_opened
    g_opened = False

def proc_close(queue_pool):
    pass

def init_log():
    return logger(BSessionCfg.log_level, BSessionCfg.log_module,
                  BSessionCfg.log_path, BSessionCfg.log_maxsize)

def init_mq():
    mq = RabbitMQClient(BSessionCfg.mq_user_name, BSessionCfg.mq_password,
                        BSessionCfg.mq_host, BSessionCfg.mq_port,
                        BSessionCfg.mq_virtual_host)

    mq.declare(BSessionCfg.mq_recv_queue, distributing)
    return mq

def main():
    signal.signal(signal.SIGINT, signal_close)
    signal.signal(signal.SIGTERM, signal_close)

    log = init_log()
    mq = init_mq()
    g_queue_pool = QueuePool(BSessionCfg.proc_work_num)

    procList = []
    for index in range(BSessionCfg.proc_work_num):
        procList.append(multiprocessing.Process(target=Worker.working,
                                                args=(Worker(index, g_queue_pool),)))
    procList.append(multiprocessing.Process(target=Sender.sending,
                                            args=(Sender(g_queue_pool, mq),)))
    procList.append(multiprocessing.Process(target=Recver.recving,
                                            args=(Recver(g_queue_pool, mq),)))

    for proc in procList:
        proc.start()

    global g_opened
    hearter = Hearter(os.getpid(), g_opened, BSessionCfg.proc_heart_intervalr, g_queue_pool)
    hearter.heart()

    proc_close(g_queue_pool, g_queue_pool)

    for proc in procList:
        proc.join()

if __name__ in '__main__':
    main()