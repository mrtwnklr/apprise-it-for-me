## Development

SHELL := /bin/bash

# ---------------------------------------------------------------------------------------------------------------------
# manage Python virtualenv

.PHONY: dev-install-virtualenv
dev-install-virtualenv: ## Install packages in Python virtualenv
	python -m pip install --quiet pipenv

	pipenv sync --dev

	pipenv run pre-commit install

.PHONY: dev-delete-virtualenv
dev-delete-virtualenv: ## Remove Python virtualenv
	pipenv --rm

# ---------------------------------------------------------------------------------------------------------------------
# run development server

.PHONY: dev-run
dev-run: dev-install-virtualenv
dev-run: ## Run a development server
	. .env ; pipenv run gunicorn --config application/gunicorn.conf.py \
															 --worker-tmp-dir /dev/shm \
															 --bind :$${GUNICORN_PORT:-8081} \
															 'manage:app'

.PHONY: dev-run-docker-compose
dev-run-docker-compose: ## Run as docker container together with an Apprise test instance
	docker-compose up

# ---------------------------------------------------------------------------------------------------------------------
# qa

.PHONY: qa-check-all-files
qa-check-all-files: dev-install-virtualenv
qa-check-all-files: ## Execute all checks on all files
	pipenv run pre-commit run --all-files
