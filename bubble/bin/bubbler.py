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

procMap = {
    'BClient': BClient.main,
    'BConfig': BConfig.main,
    'BData': BData.main,
    'BGate': BGate.main,
    'BManager': BManager.main,
    'BRoute': BRoute.main,
    'BSession': BSession.main,
    'BWall': BWall.main,
}

def help():
    print 'h/help'
    print 'r/run [BClient, BConfig, BData, BGate, BManager, BRoute, BSession, BWall]'

def main():
    op = sys.argv[1]
    if op is 'h' or op is 'help':
        help()
    elif op is 'r' or op is 'run':
        procMap[sys.argv[2]]()

if __name__ in '__main__':
    main()


