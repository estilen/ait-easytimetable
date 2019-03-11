#!/bin/sh

docker-compose down
docker-compose build
docker-compose up -d --scale api=3
