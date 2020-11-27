PYTHON=python -OO
MANAGE=python -OO manage.py

server:
	$(MANAGE) runserver

static-update:
	$(MANAGE) collectstatic --noinput

static-clear:
	$(MANAGE) collectstatic --clear --noinput

requirements:
	$(PYTHON) -m pip install -r REQUIREMENTS.txt -U

requirements-dev:
	$(PYTHON) -m pip install -r REQUIREMENTS-DEV.txt -U

install: requirements static-update
	$(MANAGE) migrate

demo:
	$(PYTHON) -m pip install -r REQUIREMENTS.txt -U
	$(MANAGE) migrate
	$(MANAGE) collectstatic --noinput
	$(MANAGE) runserver
