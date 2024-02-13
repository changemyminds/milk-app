IMAGE_NAME := milk-app
COMPOSE_FILE := script/docker-compose.yml
ENV_FILE := .env

.PHONY: flask-run
flask-run:
	FLASK_APP=app/app.py flask run

.PHONY: docker-build
docker-build:
	docker build --network=host -t $(IMAGE_NAME) -f script/Dockerfile .

.PHONY: docker-run
docker-run:
	docker run --network=host -p 5000:5000 --name=milk-app --env-file $(ENV_FILE) $(IMAGE_NAME)

.PHONY: start-infrastructure
start-infrastructure:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) up -d

.PHONY: stop-infrastructure
stop-infrastructure:
	docker-compose -f $(COMPOSE_FILE) down

.PHONY: test
test:
	python -m unittest discover -s test

# please make sure you have installed release-it tool
.PHONY: release
release:
	@release-it
