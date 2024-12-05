isort:
	isort django_tg_auth/

style:
	flake8 django_tg_auth/

types:
	mypy django_tg_auth/

check:
	make isort style types
