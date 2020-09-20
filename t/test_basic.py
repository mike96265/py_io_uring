import unittest
from socket import *
import time

from py_io_uring import IoUring

class TestBasic(unittest.TestCase):

    def setUp(self):
        server = socket(AF_INET, SOCK_STREAM, 0)
        server.bind(('127.0.0.1', 0))
        server.listen(5)
        self.target_addr = server.getsockname()
        self.server = server

        ring = IoUring()
        ring.queue_init(32, 0)
        self.ring= ring

    def connect_server(self):
        sock = socket(AF_INET, SOCK_STREAM, 0)
        sock.connect(self.target_addr)
        return sock

    def test_wait_cqe(self):
        ring = self.ring
        data = b"hello world"
        with self.connect_server() as ssock:
            csock, addr = self.server.accept()
            with csock:
                sqe = ring.get_sqe()
                sqe.prep_send(ssock, data)
                ring.submit()
                cqe = ring.wait_cqe()
                cqe = ring.peek_cqe()
                ring.cqe_seen(cqe)

    def test_set_data(self):
        ring = self.ring
        sqe = ring.get_sqe()
        sqe.prep_nop()
        sqe.set_data(self)
        ring.submit()
        cqe = ring.wait_cqe()
        ring.cqe_seen(cqe)
        self.assertEqual(cqe.get_data(), self)

    def test_prep_timeout(self):
        print("test prep timeout")
        ring = self.ring
        sqe = ring.get_sqe()
        sqe.prep_timeout(3)
        start = time.time()
        ring.submit()
        cqe = ring.wait_cqe()
        end = time.time()
        print("start: %s, end: %s, interval: %s" % (start, end, end - start))
        ring.cqe_seen(cqe)

    def tearDown(self):
        self.server.close()
        self.ring.queue_exit()


if __name__ == '__main__':
    unittest.main()
