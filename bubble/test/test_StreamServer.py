from gevent.server import StreamServer

class server:

    def __init__(self):
        self._server = StreamServer(('127.0.0.1', 5000), self.handle, backlog=128)
        self._server.start()

    def serve_forever(self):
        self._server.serve_forever()

    def handle(self, socket, address):
        while True:
            print socket.recv(1024)


s = server()
s.serve_forever()