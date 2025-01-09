#! /usr/bin/env bash

set -e
set -x

# Create database if doesn't exist
python setup_db.py

# Run migrations
alembic upgrade head

# Start FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
