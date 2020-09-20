from distutils.core import setup, Extension

ext = Extension(
    "py_io_uring", 
    sources = ['src/py_io_uring.c'],
    libraries=['uring'],
    include_dirs=['src']
)

setup(
    name="py_io_uring",
    version="0.0.1",
    description="Python wrapper liburing, have fun with io_uring and python.",
    ext_modules = [ext]
)

