# -*- coding:utf-8 -*-

import struct

class MsgPacket:

    '''
    HLV
    0xFF|0xFF|short|v
    '''

    HEAD_BIT = 255
    SHORT_MAX = 65536
    HEAD_LEN_SIZE = 4
    HEAD_LEN_FMT = '!BBH'
    BODY_FMT = 's'

    def __init__(self):
        self._stream_buffer = ''

    @staticmethod
    def pack(stream):
        """封包"""
        if stream is None:
            return None

        stream_len = len(stream)
        if stream_len >= MsgPacket.SHORT_MAX or stream_len is 0:
            return None

        fmt = MsgPacket.HEAD_LEN_FMT + str(stream_len) + MsgPacket.BODY_FMT
        return struct.pack(fmt,
                            MsgPacket.HEAD_BIT,
                            MsgPacket.HEAD_BIT,
                            stream_len,
                            stream)

    def unpack(self, stream):
        """分包&解包"""
        body_list = []
        self._stream_buffer += stream
        while True:
            if len(self._stream_buffer) <= MsgPacket.HEAD_LEN_SIZE:
                break   # 数据包小于等于消息头部长度

            head, stream_len = struct.unpack(MsgPacket.HEAD_LEN_FMT,
                                             self._stream_buffer[:MsgPacket.HEAD_LEN_SIZE])
            if head[0] is not chr(255) or head[1] is not chr(255) or stream_len is 0:
                body_list.append(None)
                break

            msg_size = MsgPacket.HEAD_LEN_SIZE + stream_len
            if len(self._stream_buffer) < msg_size:
                break   # 数组包不完整

            body_list.append(self._stream_buffer[MsgPacket.HEAD_LEN_SIZE: msg_size])
            self._stream_buffer = self._stream_buffer[msg_size:]

        # body_list中有None说明client有问题, 马上断开client段连接
        return body_list

def test():
    mp = MsgPacket()
    ss = str('0' * MsgPacket.SHORT_MAX)
    print mp.pack(ss)

    ss = str('0' * (MsgPacket.SHORT_MAX - 1))
    print mp.pack(ss)

    print mp.pack('zxcvbnm')

    nn = mp.pack('')
    print nn

test()




