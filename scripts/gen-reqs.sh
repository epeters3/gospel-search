#!/bin/bash

set -eo pipefail

# Generates the requirements files used by the docker images to install
# runtime python dependencies.

dir=$(dirname "$0") # this script's directory
declare -a dep_groups=("worker")

for group in "${dep_groups[@]}"
do
    poetry export \
        --format requirements.txt \
        --output "$dir/../requirements/$group.txt" \
        --only $group
done
