# FastAPI BootStrap (Docker version) 1.0.1

## .env demo

```
DB_USER=fastuser
DB_PASSWORD=fastpassword!
DB_HOST=pgdb
DB_NAME=fastdb
```

## Commands (Setup and Run)

### build

-   **Description:** Builds the Docker image using the specified Docker Compose file.
-   **Usage:** Run `make build` to build the Docker image. This command only builds the image and doesn't start any containers.

### rebuild

-   **Description:** Removes all containers, networks, volumes, and images, then rebuilds the Docker image and starts the containers in detached mode.
-   **Usage:** Run `make rebuild` to rebuild the image and restart the containers. This is useful when you want to start fresh with new changes.

### start

-   **Description:** Starts the Docker containers in detached mode using the specified Docker Compose file.
-   **Usage:** Run `make start` to start the containers. If the containers are already running, they will continue to run without any changes.

### restart

-   **Description:** Stops and removes the running containers, then starts them again in detached mode.
-   **Usage:** Run `make restart` to restart the containers. This is useful if you need to refresh the state of the running containers.

### stop

-   **Description:** Stops and removes the containers, networks, images, and volumes created by Docker Compose.
-   **Usage:** Run `make stop` to stop and remove all containers, networks, images, and volumes. This command is useful for cleaning up your environment.

### migrate

-   **Description:** Runs a migration script inside the FastAPI container to apply database migrations. The $(m) argument allows you to pass additional arguments to the migration script.
-   **Usage:** Run `make migrate m="additional_arguments"` to apply database migrations. Replace "additional_arguments" with any specific arguments you need for the migration script.

### clean

-   **Description:** Removes the Docker image defined by IMAGE_NAME.
-   **Usage:** Run `make clean` to remove the Docker image. This is useful if you want to delete the image from your system.

### logs

-   **Description:** Displays the logs of the FastAPI service from the last hour.
-   **Usage:** Run `make logs` to view the logs of the FastAPI service. This is helpful for debugging issues or monitoring the service.

### shell

-   **Description:** Opens a shell inside the FastAPI container for debugging purposes. The container will be removed after exiting the shell.
-   **Usage:** Run `make shell` to start a shell session inside the FastAPI container. This is useful for debugging or inspecting the running container.
