#!/bin/bash

# Crawls the online gospel library to extract all the raw html pages of the scriptures and conference talks,
# saving them all in the `pages` collection of the `gospel_search` database in MongoDB.

docker-compose -f dockerfiles/docker-compose.yaml up \
    --build \
    --force-recreate \
    --renew-anon-volumes \
    --abort-on-container-exit \
    --exit-code-from crawler \
    mongodb crawler
