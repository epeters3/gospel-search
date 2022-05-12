#!/bin/bash

# Starts the database, and an admin UI for browsing the data therein. Once started,
# the admin UI is accessible from http://0.0.0.0:8081. Also starts the Elasticsearch
# instance.

docker-compose -f dockerfiles/docker-compose.yaml up \
    --build \
    --force-recreate \
    --renew-anon-volumes \
    --abort-on-container-exit \
    mongodb mongoui elasticsearch nlp-service
