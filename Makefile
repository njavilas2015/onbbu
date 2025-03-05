include .env

VENV=/home/vscode/venv
PYTHON=python
PIP=$(VENV)/bin/pip
ENV=${PWD}.env

install:
	$(PIP) install -r requirements.txt
	$(PIP) install --upgrade pip

run: migrate
	$(PYTHON) manage.py runserver 0.0.0.0:8000

migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	
test:
	$(PYTHON) manage.py test

lint:
	$(VENV)/bin/pylint myapp

import-db:
	pv db.sql | mysql -u $(SQL_USER) -p $(SQL_PASSWORD) -h $(SQL_HOST) -P $(SQL_PORT) $(SQL_DATABASE)

export-sql:
	mysql -u $(SQL_USER) -p $(SQL_PASSWORD) -h $(SQL_HOST) -P $(SQL_PORT) $(SQL_DATABASE) > db.sql

clean:
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -delete

drop: clean
	rm db.sqlite3

shell:
	cd app && $(PYTHON) src/manage.py shell

push:
	git add .
	git commit -m "auto update"
	git push origin main

build:
	docker build -t app:local .

default:
	cd app && $(PYTHON) manage.py add_default_discounts