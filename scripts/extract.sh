#!/bin/bash

# Extracts segments (paragraphs or verses) from all the content previously
# crawled by the `crawl` step. Saves the results to the `segments` table in
# the `gospel_search` database.

docker-compose -f dockerfiles/docker-compose.yaml up \
    --build \
    --force-recreate \
    --renew-anon-volumes \
    --abort-on-container-exit \
    --exit-code-from crawler \
    mongodb extractor
