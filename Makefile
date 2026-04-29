.PHONY: run start stop status install

PY=py

run:
	$(PY) -m src run

start:
	$(PY) -m src start

stop:
	$(PY) -m src stop

status:
	$(PY) -m src status

install:
	pip install -e .



