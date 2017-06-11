# -*- coding:utf-8 -*-

class MsgXOR:

    @staticmethod
    def _xor(key, stream):
        stream_list = list(stream)
        key_len = len(key)
        stream_len = len(stream)
        for i in range(stream_len):
            c = ord(stream_list[i]) ^ ord(key[i % key_len])
            stream_list[i] = chr(c)
        return ''.join(stream_list)

    @staticmethod
    def xor_left(key, stream):
        """从key的左到右异或, 用在client发送给server"""
        return MsgXOR._xor(key, stream)

    @staticmethod
    def xor_right(key, stream):
        """从key的右到左异或, 用在server发送给client"""
        return MsgXOR._xor(key[::-1], stream)

def test():

    key = '1234567890'
    ss = 'abcdefghijklmnopqrstuvwxyz'

    s0 = MsgXOR.xor_left(key, ss)
    s1 = MsgXOR.xor_left(key, s0)
    s2 = MsgXOR.xor_right(key, ss)
    s3 = MsgXOR.xor_right(key, s2)

    print s0
    print s1
    print s2
    print s3



test()