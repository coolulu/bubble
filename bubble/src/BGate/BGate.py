# -*- coding:utf-8 -*-

from bubble.common.mq.RabbitMQClient import RabbitMQClient
import gevent
import gipc
import multiprocessing
from multiprocessing import Process
from gevent.server import StreamServer
from gevent import socket
from datetime import datetime
import time

from bubble.config import BGateCfg

sem = gevent.lock.Semaphore()
clientSet = set() #要加锁Semaphore

def closeSocket(s, sem):
    s.close()
    with sem:
        if s in clientSet:
            clientSet.remove(s)

def closeSocket(s):
    s.close()
    if s in clientSet:
        clientSet.remove(s)


def handle(socket, address):
    with sem:
        clientSet.add(socket)
    while True:
        message = socket.recv(1024)
        if len(message) == 0:
            closeSocket(socket, sem)
            break

        with sem:
            for s in clientSet:
                try:
                    if s != socket:
                        ss = str(datetime.now()) + ' ' + str(s.fileno()) + ' ' + message
                        s.sendall(ss)
                except Exception as e:
                    print e, s
                    closeSocket(s)

def writing(writer):
    while True:
        writer.put('broadcast')
        gevent.sleep(10)

def reading(reader, clientSet, sem):
    while True:
        message = reader.get()
        print message
        if len(message) != 0:
            with sem:
                print 'reading: ' + str(len(clientSet))
                for s in clientSet:
                    try:
                        ss = str(datetime.now()) + ' ' + str(s.fileno()) + ' ' + message
                        s.send(ss)
                    except Exception as e:
                        print e, s
                        closeSocket(s)

def serve_forever():
    with gipc.pipe() as (r, w):
        p = gipc.start_process(target=writing, args=(w,))
        wg = gevent.spawn(reading, r, clientSet, sem)
        server.serve_forever()
        wg.join()
        p.join()



def main_recv_msg_cb(ch, method, properties, body):
    pass

server = None

def main():
    server = StreamServer(('127.0.0.1', 5000), handle, backlog=128)
    server.start()
    for i in range(1):
        Process(target=serve_forever, args=tuple()).start()
    mq = RabbitMQClient.init_mq(BGateCfg.MQ.user_name,
                                BGateCfg.MQ.password,
                                BGateCfg.MQ.host,
                                BGateCfg.MQ.port,
                                BGateCfg.MQ.virtual_host)
    mq.declare(BGateCfg.MQ.recv_queue, main_recv_msg_cb)
    mq.recv_msg()

if __name__ in '__main__':
    main()