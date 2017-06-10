# -*- coding:utf-8 -*-

import struct

class MsgPacket:

    '''
    HLV
    0xFF|0xFF|short|v
    '''

    HEAD_BIT = 255
    SHORT_MAX = 65536

    @staticmethod
    def pack(stream):
        """封包"""
        stream_len = len(stream)
        if stream_len >= MsgPacket.SHORT_MAX:
            return None

        fmt = 'BBH' + str(stream_len) + 's'
        return struct.pack(fmt,
                            MsgPacket.HEAD_BIT,
                            MsgPacket.HEAD_BIT,
                            stream_len,
                            stream)


    def unpack(self, stream):
        """解包"""
        pass

def test():
    mp = MsgPacket()
    ss = str('0' * MsgPacket.SHORT_MAX)
    print mp.pack(ss)
    ss = str('0' * (MsgPacket.SHORT_MAX - 1))
    print mp.pack(ss)
    print mp.pack('zxcvbnm')


test()




