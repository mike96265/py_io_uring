#!/home/luvjoey/.pyenv/versions/python37-debug/bin/python
import logging
from socket import *
import sys

from py_io_uring import IoUring

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
ring = IoUring()

def listen_on(host, port):
    server = socket(AF_INET, SOCK_STREAM, 0)
    server.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    server.bind((host, port))
    server.listen(5)
    return server

def accepted(sfd, cqe=None):
    try:
        ret = cqe.getresult()
        breakpoint
        sqe = ring.get_sqe()
        sqe.prep_recv(ret, 512)
        sqe.set_data((recv, ret))
    except OSError as e:
        logging.exception("error while accept connection")
        raise e
    finally:
        sqe = ring.get_sqe()
        sqe.prep_accept(sfd)
        sqe.set_data((accepted, sfd))

        ring.submit()

def closed(fd, cqe=None):
    logging.info("connection closed: %s", fd)
    pass


def recv(fd, cqe=None):
    try:
        ret = cqe.getresult()

        if not ret:
            logging.info("closing connection: %s", fd)
            sqe = ring.get_sqe()
            sqe.prep_close(fd)
            sqe.set_data((closed, fd))
            ring.submit()
            logging.info("prepare finished closing connection: %s", fd)
            return

        sqe = ring.get_sqe()
        sqe.prep_send(fd, ret)
        sqe.set_data((written, fd, ret))

        sqe = ring.get_sqe()
        sqe.prep_recv(fd, 1024)
        sqe.set_data((recv, fd))
        ring.submit()

    except OSError as e:
        logging.exception("error while recv peer")
        raise e



def written(fd, buf, cqe=None):
    try:
        res = cqe.getresult()
        l = len(buf)
        if l < res:
            sqe = ring.get_sqe()
            sqe.prep_send(fd, buf[res:])
            sqe.set_data((written, fd, buf[res:]))
            ring.submit()
        logging.info("write to peer: %s, %s, %s", res, l, fd)
    except OSError as e:
        logging.exception("error while write peer")
        pass

def waiting():
    cq_ready = ring.cq_ready()
    sq_ready = ring.sq_ready()
    if cq_ready:
        cqes = ring.wait_cqes(cq_ready)
    else:
        cqe = ring.wait_cqe()
        cqes = (cqe, )
    for cqe in cqes:
        process_cqe(cqe)
        ring.cqe_seen(cqe)
    # cqe = ring.wait_cqe()
    # process_cqe(cqe)
    # ring.cqe_seen(cqe)


def process_cqe(cqe):
    cb, *args  = cqe.get_data()
    logging.info("calling cb: %s", cb)
    if cb and callable(cb):
        cb(*args, cqe=cqe)


def main():
    ring.queue_init(32, 0)
    server = listen_on('127.0.0.1', 8888)
    try:
        with server:
            sfd = server.fileno()
            sqe = ring.get_sqe()
            sqe.prep_accept(sfd)
            sqe.set_data((accepted, sfd))
            ring.submit()
            sqe = None
            while 1:
                waiting()
    finally:
        ring.queue_exit()


main()

