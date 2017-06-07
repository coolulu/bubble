# -*- coding:utf-8 -*-

# 基本配置
# 程序名
base_name = 'BGate'

#程序id
base_id = 0

base_ref = base_name + '_' + str(base_id)

# LOG
# 模块名
log_module = base_ref

# 日志所在路径
log_path = './log'

# 一个日志文件的最大大小,单位:B
log_maxsize = 104857600

# 日志级别('info', 'warning', 'error', 'critical')
log_level = 'info'

# MQ
# mq用户名
mq_user_name = 'admin'

# mq密码
mq_password = 'admin123'

# mq地址
mq_host = '192.168.154.130'

# mq端口
mq_port = 5672

# mq虚拟地址
mq_virtual_host = '/'

# mq接收队列
mq_recv_queue = base_ref

# PROC
proc_ip = '127.0.0.1'
proc_port = 5000

#cat /proc/sys/net/core/somaxconn
proc_backlog = 128

#工作进程数量
proc_work_num = 1

#修改进程打开最大文件描述符数量
#http://blog.csdn.net/kobejayandy/article/details/47128349

