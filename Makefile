help:
	@grep -E '^[A-Za-z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "[36m%-30s[0m %s\n", $$1, $$2}'

lint:
	black .
	isort . --profile black
	flake8 .

lint-check:
	black . --check
	isort . --check-only --profile black
	flake8 .

runserver:
	docker-compose run --rm -p 8080:8080 app python manage.py runserver 0.0.0.0:8080

migrate:
	docker-compose run --rm app python manage.py migrate

migrations:
	docker-compose run --rm app python manage.py makemigrations

test:
	docker-compose run --rm app sh -c "coverage run manage.py test --settings=config.settings.test && coverage report --fail-under=90"

coverage:
	docker-compose run --rm app sh -c "coverage run manage.py test --settings=config.settings.test && coverage report && coverage html"

shell:
	docker-compose run --rm app python manage.py shell -v 2

test-ci:
 	coverage run manage.py test --settings=config.settings.test
 	coverage report --fail-under=90
