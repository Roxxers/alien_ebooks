
# docker-compose files
PROD_DC = docker-compose.yml
DEV_DC = docker-compose.dev.yml
DOCKER_DEV = docker-compose -f $(PROD_DC) -f $(DEV_DC)
DOCKER_PROD = docker-compose -f $(PROD_DC)

build-dev:
	$(DOCKER_DEV) build

serve-dev:
	$(DOCKER_DEV) up -d

run-dev:
	$(DOCKER_DEV) up

build-prod:
	$(DOCKER_PROD) build

serve-prod:
	$(DOCKER_PROD) up -d

run-prod:
	$(DOCKER_PROD) up

