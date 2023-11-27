all: test

venv:
	python3 -m venv venv
	. venv/bin/activate && python3 -m pip install ujson

set_up: venv
	. venv/bin/activate && python3 setup.py build_ext --inplace
	. venv/bin/activate && python3 setup.py install

test: set_up
	. venv/bin/activate && python3 -m unittest discover
	. venv/bin/activate && python3 -m cProfile -s cumulative perfomance_test.py > cprofile_results.txt

clean:
	rm -rfv ./venv ./__pycache__ ./build ./cjson.egg-info ./dist ./cjson.cpython-310-x86_64-linux-gnu.so ./cprofile_results.txt