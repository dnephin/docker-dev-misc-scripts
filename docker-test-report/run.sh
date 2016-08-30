#!/bin/bash

set -e

PR=$1

if [ -z "$PR" ]; then
    >&2 echo "Usage: $0 PR_NUMBER"
    exit 1
fi

url="https://jenkins.dockerproject.org/job/Docker-PRs"
curl -s -f -f "$url/$PR/logText/progressiveHtml" | python report.py
