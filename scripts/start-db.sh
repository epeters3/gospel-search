#!/bin/bash

# Starts the databases, and admin UIs for browsing the data therein. Also starts the worker.

docker-compose -f dockerfiles/docker-compose.yaml up \
    --build \
    --force-recreate \
    --renew-anon-volumes \
    --abort-on-container-exit \
    mongodb mongoui elasticsearch elasticsearchui worker
