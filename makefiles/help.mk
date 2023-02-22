.DEFAULT_GOAL := help

COMMON_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

.PHONY: help
help:
	@grep --extended-regexp --no-filename '^([ */.a-zA-Z_-]+:.*?)?##.*$$' $(MAKEFILE_LIST) | awk --file=$(COMMON_DIR)/print-help.awk
