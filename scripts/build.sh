#!/bin/bash

cd docker/ && docker-compose --env-file ./../env/.env up --build -d
echo "Remove none images from computer"
docker rmi -f $(docker images | grep "<none>" | awk "{print \$3}")
echo "Containers running:"
docker ps --format "{{.Names}}" | sort
