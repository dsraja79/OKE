#!/bin/bash

# Start the services
docker-compose -f ./services/inventory/docker-compose.yaml up -d
docker-compose -f ./services/orders/docker-compose.yaml up -d


# Wait for the services to start up
sleep 5

# Start the web app
docker-compose -f ./web-app/docker-compose.yaml up
