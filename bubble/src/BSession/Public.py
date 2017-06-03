# -*- coding:utf-8 -*-

from bubble.config import BSessionCfg
from bubble.common.mq.RabbitMQClient import RabbitMQClient
from bubble.common.log.log import log, logger

def init_log():
    log = logger(BSessionCfg.log_level, BSessionCfg.log_module,
                 BSessionCfg.log_path, BSessionCfg.log_maxsize)

def init_mq():
    mq = RabbitMQClient(BSessionCfg.mq_user_name,
                        BSessionCfg.mq_password,
                        BSessionCfg.mq_host,
                        BSessionCfg.mq_port,
                        BSessionCfg.mq_virtual_host)
    mq.connect()
    return mq

