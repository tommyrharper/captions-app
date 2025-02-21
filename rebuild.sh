#!/bin/bash

# Stop and remove containers
docker-compose down

# Remove specific images
docker rmi captions-app_frontend
docker rmi captions-app_backend

# Rebuild and start containers
docker-compose build
docker-compose up
