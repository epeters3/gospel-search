#!/bin/bash

# Loads all the segments from MongoDB into the ElasticSearch instance.

docker-compose -f dockerfiles/docker-compose.yaml up \
    --build \
    --force-recreate \
    --renew-anon-volumes \
    --abort-on-container-exit \
    --exit-code-from embedder \
    importer
