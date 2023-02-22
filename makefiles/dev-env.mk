## Development

# ---------------------------------------------------------------------------------------------------------------------
# manage Python virtualenv

.PHONY: dev-install-virtualenv
dev-install-virtualenv: ## Install packages in Python virtualenv
	python -m pip install pipenv

	pipenv sync --dev

.PHONY: dev-delete-virtualenv
dev-delete-virtualenv: ## Remove Python virtualenv
	pipenv --rm
