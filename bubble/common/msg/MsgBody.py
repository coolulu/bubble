# -*- coding:utf-8 -*-

import json

class MsgBody:

    @staticmethod
    def to_json(obj):
        return json.dumps(obj)

    @staticmethod
    def to_object(body):
        return json.loads(body)

def test():
    m = {1: 1, 2: 2, 3: 3}
    ss = MsgBody.to_json(m)
    tt = MsgBody.to_object(ss)

    print ss
    print tt

test()

