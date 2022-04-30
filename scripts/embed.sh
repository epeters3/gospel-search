#!/bin/bash

# Computes and saves sentence embeddings for all the segments in the
# `segments` MongoDB table that don't already have embeddings.

docker-compose -f dockerfiles/docker-compose.yaml up \
    --build \
    --force-recreate \
    --renew-anon-volumes \
    --abort-on-container-exit \
    --exit-code-from embedder \
    mongodb embedder
