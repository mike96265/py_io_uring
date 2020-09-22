#### Name

py_io_uring = liburing + python


#### Table of Contents

- IoUring

  - queue_init(entries[, flag])

  - queue_exit()

  - get_sqe()

  - submit()

  - wait_cqe_nr(wait_nr)

  - wait_cqe()

  - peek_cqe()

  - cqe_seen(cqe)

  - sq_ready()

  - sq_space_left()

  - cq_ready()

  - cq_eventfd_enabled()

- Sqe

  - prep_send(fd, buf[, flag])

  - prep_recv(fd[, flag])

  - prep_connect(fd, addr)

  - prep_accept(fd[, flag])

  - prep_read(fd, length[, offset])

  - prep_write(fd, buf[, offset])

  - prep_nop()

  - prep_timeout(timeout[, count, flag])

  - prep_timeout_remove(sqe[, flag])

  - prep_cancel(sqe[, flag])

  - prep_close(fd)

  - set_data(data)

- Cqe

  - res()

  - get_data()

#### Description

**this module is still under development**

this module intend to help you write more pythonic code with liburing, you can take a look at test directory for code example.


#### Development

- OS: fedora32

- kernel: 5.8.6

- python: 3.7.8

- liburing: 0.7
