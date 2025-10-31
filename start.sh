#!/bin/bash

. venv/bin/activate

set -a
source .env
set +a

uvicorn app:app --host 127.0.0.1 --port 8080 --workers 1 --proxy-headers --forwarded-allow-ips='*'
