test: t/*.py
	python3 -m unittest t/*.py
install: src/py_io_uring.c
	python3 setup.py install
clean:
	python3 setup.py clean && rm -rf build
