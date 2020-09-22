#### Name

py_io_uring = liburing + python

#### Description

**this module is still under development**

this module intend to help you write more pythonic code with liburing, you can take a look at test directory for code example.


#### Development

- OS: fedora32

- kernel: 5.8.6

- python: 3.7.8

- liburing: 0.7


#### Documentation


```
Python Library Documentation: module py_io_uring

NAME
    py_io_uring - Python wrapper for linux async interface io_uring

CLASSES
    builtins.object
        Cqe
        IoUring
        Sqe

    class Cqe(builtins.object)
     |  Cqe Object
     |
     |  Methods defined here:
     |
     |  get_data(...)
     |      get_data() -> any
     |
     |      get data set in related sqe.
     |
     |  res(...)
     |      res() -> int
     |
     |      operation res.
     |
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.

    class IoUring(builtins.object)
     |  IoUring Object
     |
     |  Methods defined here:
     |
     |  cq_event_fd_enabled(...)
     |
     |  cq_ready(...)
     |      cq_ready() -> int
     |
     |      return the number of completed cqe in completion queue.
     |
     |  cqe_seen(...)
     |      cqe_seen(cqe) -> None
     |
     |      mark this Cqe Object as processed. must be called.
     |
     |  get_sqe(...)
     |      get_sqe() -> Sqe
     |
     |      acquire an Sqe object to describe an operation, return acquired Sqe object.
     |
     |  peek_cqe(...)
     |      peek_cqe() -> Cqe
     |
     |      peek for a completion without waiting, return the completed Cqe or None.
     |
     |  queue_exit(...)
     |      queue_exit() -> None
     |
     |      teardown io_uring instance.
     |
     |  queue_init(...)
     |      queue_init(entries[, flag]) -> None
     |
     |      setup an context for perfoming asynchronous IO.
     |
     |  sq_ready(...)
     |      sq_ready() -> int
     |
     |      return number of ready sqe in submition queue.
     |
     |  sq_space_left(...)
     |      sq_space_left() -> int
     |
     |      return number of sqe can be acquired in submition queue.
     |
     |  submit(...)
     |      submit() -> int
     |
     |      submit operations to kernel, return number of sqes submitted.
     |
     |  wait_cqe(...)
     |      wait_cqe() -> Cqe
     |
     |      waiting for a completion, return the completed Cqe.
     |
     |  wait_cqe_nr(...)
     |      wait_cqe_nr(wait_nr) -> List[Cqe]
     |
     |      waiting for wait_nr completions, return a list of completed Cqe Object.
     |
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.

    class Sqe(builtins.object)
     |  Sqe Object
     |
     |  Methods defined here:
     |
     |  convert_address(...)
     |
     |  prep_accept(...)
     |      prep_accept(fd[, flags]) -> None
     |
     |      Issue the equivalent of an accept4(2) system call.
     |
     |  prep_cancel(...)
     |      prep_cancel(sqe) -> None
     |
     |      prep an operation to cancel submitted operation.
     |
     |  prep_close(...)
     |      prep_close(fd) -> None
     |
     |      prepare an operation to close fd.
     |
     |  prep_connect(...)
     |      prep_connect(fd, addr) -> None
     |
     |      Issue the equivalent of a connect(2) system call.
     |
     |  prep_nop(...)
     |      prep_nop() -> None
     |
     |  prep_openat(...)
     |      prep_openat() -> None
     |
     |      Issue the equivalent of a openat(2) system call
     |
     |  prep_read(...)
     |      prep_read(fd, len[, flags]) -> None
     |
     |      Issue the equivalent of a read(2) system call.
     |
     |  prep_recv(...)
     |      prep_recv(fd, len[, flags]) -> None
     |
     |      Issue the equivalent of recv(2) system call.
     |
     |  prep_send(...)
     |      prep_send(fd, buf[, flags]) -> None
     |
     |      Issue the equivalent of a send(2) system call.
     |
     |  prep_timeout(...)
     |      prep_timeout(timeout[, flags]) -> None
     |
     |      prepare a timeout operation
     |
     |  prep_timeout_remove(...)
     |      prep_timeout_remove(sqe[, flags]) -> None
     |
     |      prepare an attempt to remove an existing timeout operation.
     |
     |  prep_write(...)
     |      prep_write(fd, buf[, flags]) -> None
     |
     |      Issue the equivalent of a write(2) system call.
     |
     |  set_data(...)
     |      set_data(data) -> None
     |
     |      set the data related to this sqe, can be reached by related cqe.
     |
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
```

