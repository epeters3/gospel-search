#!/bin/bash

# Starts the services needed to perform actual gospel library searching.

docker compose -f dockerfiles/docker-compose.yaml up \
    --build \
    --force-recreate \
    --renew-anon-volumes \
    --abort-on-container-exit \
    mongodb elasticsearch nlp-service proxy-service
