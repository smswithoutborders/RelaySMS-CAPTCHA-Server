#!/bin/bash

. venv/bin/activate

uvicorn main:app --host 127.0.0.1 --port 8080 --workers 1 --proxy-headers --forwarded-allow-ips='*'
