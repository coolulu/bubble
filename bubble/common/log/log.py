# -*- coding=utf-8 -*-

# 从配置文件读取日志配置
# 在日志目录下按天生成日志文件，并限制每个文件的大小
#
# 配置文件格式如下：

# log_module=log
# log_path=
# log_maxsize=1073741824
# log_level=debug


import os, sys, time
import logging
import datetime as dt
from datetime import date
import sys

reload(sys)
sys.setdefaultencoding('utf8')

g_logger = None
g_handler = None


class Date_Size_File_Handler(logging.Handler):
    def __init__(self, level):
        super(Date_Size_File_Handler, self).__init__(level)
        self._date = date.today()
        self._current_size = 0
        self._max_size = 1000 * 1024 * 1024  # 文件最大: 1G
        self._backup_count = 0
        self._log_path = os.path.join(os.getcwd(), "../log/")
        self._module = "log"
        self._file = None

    def set_log_path(self, path):
        self._log_path = path

    def set_module(self, module):
        self._module = module

    def module(self):
        return self._module

    def set_max_size(self, max_size):
        self._max_size = max_size

    def reset(self):
        if self._file:
            self._file.close()
        self._current_size = 0
        self._backup_count = 0
        self._file = None

    def _calc_file_name(self):
        if not os.path.exists(self._log_path):
            os.mkdir(self._log_path)
        str = "%s/%s%s_%d" % (self._log_path, self._module, self._date.strftime("%Y%m%d"), time.time());
        if self._backup_count > 0:
            str = str + "_%d.log" % (self._backup_count)
        else:
            str = str + ".log"

        if os.path.exists(str) and os.path.getsize(str) >= self._max_size:
            self._backup_count += 1
            return self._calc_file_name()
        return str

    def emit(self, record):
        if self._date != date.today() or self._current_size >= self._max_size:
            self._file.close()
            self._file = None
            self._current_size = 0
            if self._date != date.today():
                self._date = date.today()
                self._backup_count = 0
            else:
                self._backup_count += 1

        if not self._file:
            str = self._calc_file_name()
            self._file = open(str, "a+")

        utf8_str = self.format(record).encode("utf-8")
        self._file.write(utf8_str)
        self._file.write("\n")
        self._file.flush()
        self._current_size += len(utf8_str) + 1  # warning::假设换行符占1个字节
        # print utf8_str;


# 用于显示日期的毫秒
class MyFormatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s


# 根据配置文件设置日志, 之后使用logger记录日志
level_mapping = {
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "info": logging.INFO,
    "critical": logging.CRITICAL
}


def setup(log_level, log_module, log_path, log_size):
    nlevel = logging.DEBUG
    if level_mapping.has_key(log_level):
        nlevel = level_mapping[log_level]

    datefmt = "%Y-%m-%d %H:%M:%S .%f"
    logfmt = "%(asctime)s %(threadName)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"

    logging.basicConfig(level=nlevel, format=logfmt, datefmt=datefmt);

    h = Date_Size_File_Handler(0)
    h.set_module(log_module)
    h.set_max_size(log_size)
    if len(log_path) > 0:
        h.set_log_path(log_path)  # 不配置则取默认值

    # formatter = logging.Formatter(logfmt, datefmt);
    formatter = MyFormatter(logfmt)
    h.setFormatter(formatter)
    h.setLevel(nlevel)

    global g_handler
    g_handler = h

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(nlevel)

    global g_logger
    g_logger = logging.getLogger(log_module)  # 注意: 加了模块名，其它库的日志就不记录了
    g_logger.addHandler(h)
    g_logger.addHandler(console)

    ##去除root logger的控制台输出，其它模块打印的日志就看不到啦## 视情况注释掉下面的几行##
    logger = logging.getLogger()
    lhStdout = logger.handlers[0]
    logger.removeHandler(lhStdout)


#### 接口在此 ####
def logger(log_level, log_module, log_path, log_size):
    global g_logger
    if not g_logger:
        setup(log_level, log_module, log_path, log_size)
    return g_logger


# def handler():
#     global g_handler
#     if not g_handler:
#         setup()
#     return g_handler
#
#
# Log = logger()
# Log_Handler = handler()

# ### test  ####
# def __test():
#     setup()
#     for x in range(1024):
#         logger().info(x);
#         logger().debug("this is debug msg")
#         logger().info("this is info msg ")
#         logger().warn("this is warning msg 等待")
#         logger().warn("this is 22222 warning msg")
#
# if __name__ == "__main__":
#     __test();
#     logging.info('h');


