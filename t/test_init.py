import unittest
from py_io_uring import IoUring

class TestInit(unittest.TestCase):

    def test_queue_init(self):
        ring = IoUring()
        ring.queue_init(32, 0)
        ring.queue_exit()

    def test_queue_init_exception(self):
        ring = IoUring()
        self.assertRaises(OSError, ring.queue_init, -1, 0)


if __name__ ==  '__main__':
    unittest.main()

