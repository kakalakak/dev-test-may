UNAME = $(shell uname -s)

PYTHON = python3

.PHONY: install
install:
	./venv/bin/pip install -r requirements.txt

.PHONY: venv
venv:
	$(PYTHON) -m virtualenv venv  --python=$(PYTHON)

.PHONY: spacy
spacy:
	./venv/bin/python -m spacy download en_core_web_lg

.PHONY: run
run:
	./venv/bin/python manage.py runserver

.PHONY: migrate
migrate:
	./venv/bin/python manage.py migrate
