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
        print(self.target_addr)
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
                    sqe.prep_send(ssock.fileno(), d)
                    ring.submit()
                    cqes = ring.wait_cqe()
                    self.assertEqual(len(cqes), 1)
                    ring.cqe_seen(cqe)
                    cdata = csock.recv(1024)
                    self.assertEqual(cdata, data)


    def test_connect(self):
        ring = self.ring
        sqe = ring.get_sqe()
        csock = socket(AF_INET, SOCK_STREAM, 0)
        with csock:
            sqe.prep_connect(csock.fileno(), self.target_addr)
            ring.submit()
            cqe = ring.get_cqe()
            ring.cqe_seen(cqe)
            ssock, addr = self.server.accept()
            with ssock:
                self.assertEqual(csock.getsockname(), addr)
                self.comunicate(ssock, csock)

    def test_accept(self):
        ring = self.ring
        with self.connect_server() as csock:
            sqe = ring.get_sqe()
            sqe.prep_accept(self.server.fileno())
            ring.submit()
            cqe = ring.wait_cqe()
            cfd = cqe.res()
            ring.cqe_seen(cqe)
            ssock = socket(fileno=cfd)
            with ssock:
                self.comunicate(ssock, csock)

    def test_prep_recv_getresult(self):
        ring = self.ring
        sqe = ring.get_sqe()
        with self.connect_server() as ssock:
            csock, addr = self.server.accept()
            with csock:
                csock.send(b"hello world")
                sqe.prep_recv(ssock.fileno(), 1024, 0)
                ring.submit()
                cqe = ring.wait_cqe()
                self.assertEqual(cqe.getresult(), b"hello world")
                ring.cqe_seen(cqe)
    
    def test_wait_cqes(self):
        ring = self.ring
        with self.connect_server() as ssock:
            csock, addr = self.server.accept()
            with csock:
                sqe = ring.get_sqe()
                sqe.prep_recv(ssock.fileno(), 1024)
                sqe.set_data(2)

                sqe = ring.get_sqe()
                sqe.prep_accept(self.server.fileno())
                sqe.set_data(1)

                ring.submit()
                print("start wait")
                cqes = ring.wait_cqes(2)
                print("end wait")


    def tearDown(self):
        self.server.close()
        self.ring.queue_exit()


if __name__ == '__main__':
    unittest.main()
