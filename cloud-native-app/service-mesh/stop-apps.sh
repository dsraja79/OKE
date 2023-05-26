#!/bin/bash

# Start the services
docker-compose -f ./services/inventory/docker-compose.yaml down
docker-compose -f ./services/orders/docker-compose.yaml down
docker-compose -f ./web-app/docker-compose.yaml down

# Remove all containers
docker container prune -f
