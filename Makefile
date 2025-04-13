.PHONY: build run stop clean test dev docker-push docker-login help

# Include environment variables from .env file if it exists
-include .env

# Docker image settings (with defaults that can be overridden by .env)
IMAGE_NAME = fastapi-todo-demo
VERSION ?= latest
DOCKER_REGISTRY ?= docker.io
DOCKER_USERNAME ?= username

# Application settings
APP_PORT ?= 8000
HOST_PORT ?= 8000

# Help command
help:
	@echo "Available commands:"
	@echo "  make build         - Build the Docker image"
	@echo "  make run           - Run the Docker container"
	@echo "  make stop          - Stop the Docker container"
	@echo "  make clean         - Remove the Docker container and image"
	@echo "  make test          - Run tests"
	@echo "  make dev           - Start the development server with hot reload"
	@echo "  make docker-login  - Login to Docker registry"
	@echo "  make docker-push   - Push the Docker image to registry"
	@echo "  make env-setup     - Create .env file from .env.example"
	@echo "  make help          - Show this help message"

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

# Run the Docker container
run:
	docker run -d --name $(IMAGE_NAME) -p $(HOST_PORT):$(APP_PORT) $(IMAGE_NAME):$(VERSION)

# Stop the Docker container
stop:
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true

# Remove the Docker container and image
clean: stop
	docker rmi $(IMAGE_NAME):$(VERSION) || true

# Run tests
test:
	pytest

# Start the development server with hot reload
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port $(APP_PORT)

# Login to Docker registry
docker-login:
	@echo "Logging in to Docker registry..."
	@if [ -z "$(DOCKER_PASSWORD)" ]; then \
		docker login $(DOCKER_REGISTRY) -u $(DOCKER_USERNAME); \
	else \
		echo "$(DOCKER_PASSWORD)" | docker login $(DOCKER_REGISTRY) -u $(DOCKER_USERNAME) --password-stdin; \
	fi

# Tag and push the Docker image to registry
docker-push: docker-login build
	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_REGISTRY)/$(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)
	docker push $(DOCKER_REGISTRY)/$(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)

# Create .env file from .env.example if it doesn't exist
env-setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env file created from .env.example. Please update with your values."; \
	else \
		echo ".env file already exists."; \
	fi

# Default command
all: help