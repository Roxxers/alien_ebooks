
BUILD_DEV_WARNING = "Do not run without first building the normal image with 'make build'"

# docker-compose files
PROD_DC = docker-compose.yml
DEV_DC = docker-compose.dev.yml
DOCKER_DEV = docker-compose -f $(PROD_DC) -f $(DEV_DC)
DOCKER_PROD = docker-compose -f $(PROD_DC)

.PHONY: install-deps remove-make-deps

# Requires Python-pip, Node, and NPM
install-deps:
	python3 -m pip install pipenv && \
	pipenv install && \
	npm install && \
	npx webpack -p

install-deps-dev:
	python3 -m pip install pipenv && \
	pipenv install -d && \
	npm install --dev && \
	npx webpack -p

remove-make-deps:
	npm ls -p --depth=0 | awk -F/ '/node_modules/ && !/\/npm$/ {print $NF}' | xargs npm rm &&\
	npm cache clean --force

# For use with Dockerfile
docker-install-deps : install-deps remove-make-deps

build-dev:
	echo $(BUILD_DEV_WARNING) && \
	$(DOCKER_DEV) build

serve-dev:
	$(DOCKER_DEV) up -d

run-dev:
	$(DOCKER_DEV) up

build:
	$(DOCKER_PROD) build

serve:
	$(DOCKER_PROD) up -d

run:
	$(DOCKER_PROD) up

stop:
	docker-compose down

