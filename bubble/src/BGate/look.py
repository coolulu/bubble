# -*- coding:utf-8 -*-
import gevent
import gipc
import multiprocessing
from multiprocessing import Process
from gevent.server import StreamServer
from gevent import socket
from datetime import datetime
import time

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
        print 'handle: ' + str(len(clientSet))
        print 'connect: ' + multiprocessing.current_process().name

    while True:
        message = socket.recv(1024)
        if len(message) == 0:
            closeSocket(socket, sem)
            break

        with sem:
            for s in clientSet:
                try:
                    # print socket
                    if s != socket:
                        ss = str(datetime.now()) + ' ' + str(s.fileno()) + ' ' + message
                        print ss
                        s.sendall(ss)
                except Exception as e:
                    print e, s
                    closeSocket(s)

def writing(writer):
    while True:
        writer.put('broadcast\n')
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
                        print ss
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

#backlog：cat /proc/sys/net/core/somaxconn
server = StreamServer(('127.0.0.1', 5000), handle, backlog=128)
server.start()
for i in range(1):
    Process(target=serve_forever, args=tuple()).start()

time.sleep(100000000)
