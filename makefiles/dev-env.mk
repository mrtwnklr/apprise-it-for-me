## Development

# ---------------------------------------------------------------------------------------------------------------------
# manage Python virtualenv

.PHONY: dev-install-virtualenv
dev-install-virtualenv: ## Install packages in Python virtualenv
	python -m pip install --quiet pipenv

	pipenv sync --dev

.PHONY: dev-delete-virtualenv
dev-delete-virtualenv: ## Remove Python virtualenv
	pipenv --rm

# ---------------------------------------------------------------------------------------------------------------------
# run development server

.PHONY: dev-run
dev-run: dev-install-virtualenv
dev-run: ## Run a development server
	FLASK_APP=manage.py pipenv run flask run
