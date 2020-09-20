#define PY_SSIZE_T_CLEAN
#include <Python.h>

static int inline SockObject_fileno(PyObject *sock)
{
    PyObject *sockfd;
    int fd;
    sockfd = PyObject_CallMethod(sock, "fileno", NULL);
    if (sockfd == NULL) {
        return 0;
    }
    fd = PyLong_AS_LONG(sockfd);
    Py_DECREF(sockfd);
    return fd;
}

