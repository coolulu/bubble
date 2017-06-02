# -*- coding:utf-8 -*-

import sys

from bubble.src.BClient import BClient
from bubble.src.BConfig import BConfig
from bubble.src.BData import BData
from bubble.src.BGate import BGate
from bubble.src.BManager import BManager
from bubble.src.BRoute import BRoute
from bubble.src.BSession import BSession
from bubble.src.BWall import BWall

def help():
    print ['h/help']
    print ['r/run BClient/BConfig/BData/BGate/BManager/BRoute/BSession/BWall']

def run(proc_name):
    if proc_name is 'BClient':
        BClient.main()
    elif proc_name is 'BConfig':
        BConfig.main()
    elif proc_name is 'BData':
        BData.main()
    elif proc_name is 'BGate':
        BGate.main()
    elif proc_name is 'BManager':
        BManager.main()
    elif proc_name is 'BRoute':
        BRoute.main()
    elif proc_name is 'BSession':
        BSession.main()
    elif proc_name is 'BWall':
        BWall.main()

def main():
    op = sys.argv[1]
    if op is 'h' or op is 'help':
        help()
    elif op == 'r' or op == 'run':
        run(sys.argv[2])

if __name__ in '__main__':
    main()


