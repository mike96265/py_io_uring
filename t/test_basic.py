import unittest
from socket import *
import time

from py_io_uring import IoUring

class TestBasic(unittest.TestCase):

    def setUp(self):
        ring = IoUring()
        ring.queue_init(32, 0)
        self.ring= ring

    def test_sp_ready(self):
        ring = self.ring

        nready = ring.sq_ready()
        self.assertEqual(nready, 0)

        sqe = ring.get_sqe()
        sqe.prep_nop()

        nready = ring.sq_ready()
        self.assertEqual(nready, 1)

        ring.submit()

        nready = ring.sq_ready()
        self.assertEqual(nready, 0)

        cqe = ring.wait_cqe()
        ring.cqe_seen(cqe)

    def test_sp_space_left(self):
        ring = self.ring

        nleft = ring.sq_space_left()
        self.assertEqual(nleft, 32)

        sqe = ring.get_sqe()
        sqe.prep_nop()

        nleft = ring.sq_space_left()
        self.assertEqual(nleft, 31)

        ring.submit()

        nleft = ring.sq_space_left()
        self.assertEqual(nleft, 32)

    def test_cq_ready(self):
        ring = self.ring

        nready = ring.cq_ready()
        self.assertEqual(nready, 0)

        sqe = ring.get_sqe()
        sqe.prep_nop()
        ring.submit()
        cqe = ring.wait_cqe()

        nready = ring.cq_ready()
        self.assertEqual(nready, 1)

        ring.cqe_seen(cqe)

        nready = ring.cq_ready()
        self.assertEqual(nready, 0)


    def test_wait_cqe(self):
        ring = self.ring
        sqe = ring.get_sqe()
        sqe.prep_nop()
        ring.submit()
        wcqe = ring.wait_cqe()
        pcqe = ring.peek_cqe()
        self.assertEqual(wcqe, pcqe)
        ring.cqe_seen(wcqe)

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
        print("testing prep timeout, delay: 1s")
        ring = self.ring
        sqe = ring.get_sqe()
        sqe.prep_timeout(1)
        start = time.time()
        ring.submit()
        cqe = ring.wait_cqe()
        end = time.time()
        print("start: %s, end: %s, interval: %s" % (start, end, end - start))
        self.assertEqual(1, int(end - start))
        ring.cqe_seen(cqe)

    def tearDown(self):
        self.ring.queue_exit()


if __name__ == '__main__':
    unittest.main()
