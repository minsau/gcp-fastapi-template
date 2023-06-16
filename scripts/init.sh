#! /usr/bin/env bash

# Let the DB start
python scripts/backend_pre_start.py

# If its necessary to remove versions
python scripts/restore_alembic_versions.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python scripts/initial_data.py
