# -*- coding:utf-8 -*-

import gevent

'''
客户端连接池
'''
class ClientPool:

    def __init__(self):
        self._clients = set()
        self._sem = gevent.lock.Semaphore()

    def append(self, sockfd):
        with self._sem:
            if sockfd not in self._clients:
                self._clients.add(sockfd)
                return True

        return False

    def close(self, sockfd):
        sockfd.close()
        with self._sem:
            if sockfd in self._clients:
                self._clients.remove(sockfd)
                return True

        return False

    def send(self, sockfd, msg):
        with self._sem:
            if sockfd in self._clients:
                try:
                    sockfd.sendall(msg)
                    return True
                except Exception as e:
                    self._close(sockfd)

        return False

    def _close(self, sockfd):
        sockfd.close()
        if sockfd in self._clients:
            self._clients.remove(sockfd)


