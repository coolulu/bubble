# -*- coding:utf-8 -*-

import gevent

'''
客户端连接池
'''
class ClientPool:

    def __init__(self):
        self._clients = set()
        self._sem = gevent.lock.Semaphore()

    def appendClient(self, sockfd):
        with self._sem:
            if sockfd not in self._clients:
                self._clients.add(sockfd)

    def closeClient(self, sockfd):
        sockfd.close()
        with self._sem:
            if sockfd in self._clients:
                self._clients.remove(sockfd)

    def send(self, sockfd, msg):
        with self._sem:
            if sockfd in self._clients:
                try:
                    sockfd.sendall(msg)
                except Exception as e:
                    self._closeClient(sockfd)

    def _closeClient(self, sockfd):
        sockfd.close()
        if sockfd in self._clients:
            self._clients.remove(sockfd)


