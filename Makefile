# Define variables for Docker-related tasks
IMAGE_NAME = fastapi_bootstrap
DOCKER_COMPOSE_FILE = docker-compose.yml

# Build the Docker image
build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build

# Rebuild the Docker image and start the containers
rebuild:
	docker compose -f $(DOCKER_COMPOSE_FILE) down --rmi all
	docker compose -f $(DOCKER_COMPOSE_FILE) build
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Run the Docker container
start:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Restart Docker container
restart:
	docker compose -f $(DOCKER_COMPOSE_FILE) down
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop and remove containers, networks, images, and volumes
stop:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

# Create migration
migrate:
	docker compose run fastapi /scripts/migrate-db.sh $(m)

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME)

# Display logs of the FastAPI service
logs:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs --since=1h fastapi

# Run a shell inside the FastAPI container for debugging
shell:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm fastapi sh
