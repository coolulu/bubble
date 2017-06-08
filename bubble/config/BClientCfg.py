# -*- coding:utf-8 -*-

# 基本配置
class Base:
    # 程序名
    name = 'BClient'

# LOG
class Log:
    # 模块名
    module = Base.name

    # 日志所在路径
    path = './log'

    # 一个日志文件的最大大小,单位:B
    maxsize = 104857600

    # 日志级别('info', 'warning', 'error', 'critical')
    level = 'info'

