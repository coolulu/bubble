# -*- coding:utf-8 -*-

# 基本配置
class Base:
    # 程序名
    name = 'BManager'

    #程序id
    id = 0

    ref = name + '_' + str(id)

# LOG
class Log:
    # 模块名
    module = Base.ref

    # 日志所在路径
    path = './log'

    # 一个日志文件的最大大小,单位:B
    maxsize = 104857600

    # 日志级别('info', 'warning', 'error', 'critical')
    level = 'info'

# MQ
class MQ:
    # mq用户名
    user_name = 'admin'

    # mq密码
    password = 'admin123'

    # mq地址
    host = '192.168.154.130'

    # mq端口
    port = 5672

    # mq虚拟地址
    virtual_host = '/'

    # mq接收队列
    recv_queue = Base.ref
