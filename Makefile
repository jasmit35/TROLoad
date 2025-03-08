.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv sync --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@uv run deptry .

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean up any crap from previous builds
	@echo "🚀 Removing any crap from previous builds..."
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: publish
publish: ## Publish a release to PyPI.
	@echo "🚀 Publishing: Dry run."
	@uvx --from build pyproject-build --installer uv
	@echo "🚀 Publishing."
	@uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@echo "🚀 Generating local PDF documentation"
	@pandoc --toc=true -o '/Volumes/SharedSpace/Users/jeff/Project Documentation/Active/TROLoad System Guide.pdf' 'docs/TROLoad System Guide.md'
	@pandoc --toc=true -o "/Volumes/SharedSpace/Users/jeff/Project Documentation/Active/TROLoad User's Guide.pdf" "docs/TROLoad User's Guide.md"
	@uv run mkdocs serve

################################################################################
#
#  Docker stuff
#
################################################################################

app_version := 'feature_v1.0.0'
environment := 'devl'

.PHONY: dr-build
dr-build: clean-build ## Build our Docker container
	@echo "🚀  Building our docker image,,,"
	@export DOCKER_BUILDKIT=1
	@docker image build -t jasmit/troloadtrans:$(app_version) .
	#  @echo "🚀  Running docker scout quickview..."
	#  @docker scout quickview
	#  @echo "🚀  Running docker scout cves..."
	#  @docker scout cves local://jasmit/troloadtrans:$(app_version)

.PHONY: dr-run
dr-run: ## Run this project's container
	- rm ./logs/*
	- rm ./reports/*
	- rm ./stage/*
	- cp -R /Volumes/SharedSpace/TROStage/devl/*.xlsx ./stage/
	@echo "🚀  Running the container..."
	@docker container run -it --rm \
		--mount type=bind,source=./logs,target=/opt/app/troloadtrans/logs \
		--mount type=bind,source=./reports,target=/opt/app/troloadtrans/reports \
		--mount type=bind,source=./stage,target=/opt/app/troloadtrans/stage \
		jasmit/troloadtrans:$(app_version) -e $(environment) 

.PHONY: dr-bash
dr-bash:
	@echo "🚀  Cionnecting to running docker container..."
	@docker container run --rm -it --entrypoint /bin/bash -v ./logs:/opt/app/troload/logs -v ./reports:/opt/app/troload/reports -v ./stage:/opt/app/troload/stage jasmit/troloadtrans:latest
	@docker ps --all

.PHONY: dr-get-ip
dr-get-ip:
	@echo "🚀  Cionnecting to running docker container..."
	@docker inspect --format '{{ .NetworkSettings.IPAddress }}' jasmit/troloadtrans:latest

.PHONY: dr-status
dr-status:
	@echo "🚀  Checking the status of all docker containers..."
	@docker ps --all

.PHONY: dr-push-image
dr-push-image:
	docker push jasmit/troloadtrans:${app_version}

################################################################################

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
#
# docker container run --rm -ti 2a236efc3f06 /bin/bash
#


