#!/bin/bash
set -e

echo "Container is running!!!"
uvicorn app:app --port 8000 --host 0.0.0.0