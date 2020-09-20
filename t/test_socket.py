import unittest
from socket import *

from py_io_uring import IoUring

class TestSocket(unittest.TestCase):

    def setUp(self):
        server = socket(AF_INET, SOCK_STREAM, 0)
        server.bind(('127.0.0.1', 0))
        server.listen(5)
        self.server = server
        self.target_addr = server.getsockname()
        ring = IoUring()
        ring.queue_init(32, 0)
        self.ring = ring

    def connect_server(self):
        sock = socket(AF_INET, SOCK_STREAM, 0)
        sock.connect(self.target_addr)
        return sock

    def comunicate(self, c, s):
        data = b"hello world"
        c.send(data)
        self.assertEqual(s.recv(1024), data)
        s.send(data)
        self.assertEqual(c.recv(1024), data)

    def test_send(self):
        ring = self.ring
        data = b"hello world"

        with self.connect_server() as ssock:
            csock, addr = self.server.accept()
            with csock:
                for cast in (bytes, bytearray, memoryview):
                    sqe = ring.get_sqe()
                    d = cast(data)
                    sqe.prep_send(ssock, d)
                    ring.submit()
                    cqes = ring.wait_cqe_nr(1)
                    self.assertEqual(len(cqes), 1)
                    ring.cqe_seen(cqes[0])
                    cdata = csock.recv(1024)
                    self.assertEqual(cdata, data)


    def test_connect(self):
        ring = self.ring
        sqe = ring.get_sqe()
        csock = socket(AF_INET, SOCK_STREAM, 0)
        with csock:
            sqe.prep_connect(csock, self.target_addr)
            ring.submit()
            ssock, addr = self.server.accept()
            with ssock:
                self.assertEqual(csock.getsockname(), addr)
                self.comunicate(ssock, csock)

    def test_accept(self):
        ring = self.ring
        with self.connect_server() as csock:
            sqe = ring.get_sqe()
            sqe.prep_accept(self.server)
            ring.submit()
            cqe = ring.wait_cqe()
            cfd = cqe.res()
            ssock = socket(fileno=cfd)
            with ssock:
                self.comunicate(ssock, csock)


    def tearDown(self):
        self.server.close()
        self.ring.queue_exit()


if __name__ == '__main__':
    unittest.main()
