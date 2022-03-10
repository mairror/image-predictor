SHELL := /usr/bin/bash
.DEFAULT_GOAL := help

# AutoDoc
# -------------------------------------------------------------------------
.PHONY: help
help: ## This help. Please refer to the Makefile to more insight about the usage of this script.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help

# Docker
# -------------------------------------------------------------------------

# PREDICTOR
# -------------------------------------------------------------------------
.PHONY: build-docker-predictor
build-docker-predictor: ## Build the predictor Dockerfile. Optional variables BUILDKIT, DOCKER_PREDICTOR_IMAGE and DOCKER_PREDICTOR_TAG
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_PREDICTOR_IMAGE=$(or $(DOCKER_PREDICTOR_IMAGE),mairror-predictor) \
		DOCKER_PREDICTOR_TAG=$(or $(DOCKER_PREDICTOR_TAG),test) && \
	docker build -t $$DOCKER_PREDICTOR_IMAGE:$$DOCKER_PREDICTOR_TAG .
.DEFAULT_GOAL := build-docker-predictor

.PHONY: lint-docker-predictor
lint-docker-predictor: ## Lint the predictor Dockerfile
	docker run --rm -i -v ${PWD}:/hadolint --workdir=/hadolint hadolint/hadolint < Dockerfile
.DEFAULT_GOAL := lint-docker-predictor

.PHONY: run-docker-predictor
run-docker-predictor: ## Run the predictor isolated. Optional variables BUILDKIT, DOCKER_PREDICTOR_IMAGE and DOCKER_PREDICTOR_TAG
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_PREDICTOR_IMAGE=$(or $(DOCKER_PREDICTOR_IMAGE),mairror-predictor) \
		DOCKER_PREDICTOR_TAG=$(or $(DOCKER_PREDICTOR_TAG),test) && \
	docker run --rm --name $$DOCKER_PREDICTOR_IMAGE --env-file .env -p 8000:8000 $$DOCKER_PREDICTOR_IMAGE:$$DOCKER_PREDICTOR_TAG
.DEFAULT_GOAL := run-docker-predictor

# Python
# -------------------------------------------------------------------------

# Cache
# -------------------------------------------------------------------------
.PHONY: clean-pyc
clean-pycache: ## Clean pycache files

	find . -name '__pycache__' -exec rm -rf {} +
.DEFAULT_GOAL := clean-pyc
