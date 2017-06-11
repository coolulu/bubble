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

            header = struct.unpack(MsgPacket.HEAD_LEN_FMT,
                                   self._stream_buffer[:MsgPacket.HEAD_LEN_SIZE])
            if header[0] is not MsgPacket.HEAD_BIT or header[1] is not MsgPacket.HEAD_BIT or header[2] is 0:
                self._stream_buffer = ''  # 清空buffer
                body_list.append(None)
                break

            msg_size = MsgPacket.HEAD_LEN_SIZE + header[2]
            if len(self._stream_buffer) < msg_size:
                break   # 数组包不完整

            body_list.append(self._stream_buffer[MsgPacket.HEAD_LEN_SIZE: msg_size])
            self._stream_buffer = self._stream_buffer[msg_size:]

        # body_list中有None说明client有问题, 马上断开client段连接
        return body_list




def test1():
    ss = str('0' * MsgPacket.SHORT_MAX)
    print MsgPacket.pack(ss)

    ss = str('0' * (MsgPacket.SHORT_MAX - 1))
    print MsgPacket.pack(ss)

    print MsgPacket.pack('zxcvbnm')

    nn = MsgPacket.pack('')
    print nn

def test2():
    s0 = '1234567890'
    p0 = MsgPacket.pack(s0)
    print p0

    s1 = 'zxcvbnmasdfghjklqwertyuiop'
    p1 = MsgPacket.pack(s1)
    print p1

    p = p1 + p0

    t0 = p[:20]
    t1 = p[20:25]
    t2 = p[25:35]
    t3 = p[35:]

    mp = MsgPacket()
    up = mp.unpack(t0)
    print up
    up = mp.unpack(t1)
    print up
    up = mp.unpack(t2)
    print up
    up = mp.unpack(t3)
    print up

    perror = p0 + 'aaaaa'
    up = mp.unpack(perror)
    print up

    for s in p:
        up = mp.unpack(s)
        if len(up) is not 0:
            print up

    up = mp.unpack(p)
    print up

# test1()
test2()



