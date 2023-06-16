# FastAPI&GCP Template

This project serves as a boilerplate for future web applications built with FastAPI.

## Table of Contents
- [Requirements](#requirements)
- [Environment Variables](#environment-variables)
- [Development](#development)
- [Continuous Integration](#continuous-integration)
- [Monitoring](#monitoring)
- [Database Migration](#database-migration)
- [Deployment](#deployment)

## Requirements
The following tools are needed for this project:
- [Pyenv](https://github.com/pyenv/pyenv)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)

## Environment Variables
This project uses environment variables for configuration. You need to create a `.env` file in the root directory of the project. Use the `.env.dist` file as a base.

| Variable | Description |
| -------- | ----------- |
| POSTGRES_DB | The name of your PostgreSQL database. |
| POSTGRES_USER | The username of your PostgreSQL database. |
| POSTGRES_PASSWORD | The password for your PostgreSQL database. |
| POSTGRES_SERVER | The server address of your PostgreSQL database. |
| POSTGRES_PORT | The port of your PostgreSQL server. |
| SENTRY_DSN | Your Sentry DSN for error logging. |
| FIRST_SUPERUSER | The email of the initial superuser. |
| FIRST_SUPERUSER_PASSWORD | The password of the initial superuser. |
| USE_CLOUD_TASKS | Whether or not to use Google Cloud Tasks. |
| GCP_HIGH_PRIORITY_QUEUE_ID | The ID of the high priority queue in Google Cloud Tasks. |
| USE_GCP | Whether or not to use Google Cloud Platform. |
| GCP_PROJECT_ID | Your Google Cloud Platform project ID. |
| GCP_REGION | Your Google Cloud Platform region. |
| GCP_SECRET_ID | Your Google Cloud Platform secret ID. |
| GCLOUD_SERVICE_KEY | Your Google Cloud service account key. |
| SERVICE_ACCOUNT_EMAIL | Your Google Cloud service account email. |
| CORE_IMAGE_NAME | The name of your Docker image. |
| TAG | The tag for your Docker image. |
| PROJECT_NAME | The name of your project. |

## Development
The development workflow uses Docker to run the project and its dependencies. It also includes a `dev` script to run the server, perform tests, and handle migrations. See [Makefile](#makefile) and [dev script](#dev-script) for more details.

## Continuous Integration
The project uses [Circle CI](https://circleci.com/) for continuous integration. You need to connect your Github account with Circle CI to track the progress of your tasks.

The Circle CI workflow consists of the following steps:
- Linting the codebase.
- Running the tests.
- Building the Docker image.
- Publishing the Docker image to Google Container Registry.
- Deploying the application on Google Cloud Run.

## Monitoring
This project uses [Sentry](https://sentry.io/welcome/) for tracking unhandled errors. Make sure to set the `SENTRY_DSN` environment variable.

## Database Migration
The project uses Alembic for database migration. You can run migrations in both 'online' and 'offline' modes. Refer to the Alembic `env.py` script for more details.

## Deployment
This project is configured to be deployed on Google Cloud Run using Google Container Registry. You need to configure your Google Cloud credentials and other related environment variables to successfully deploy your application.

This project should be considered as an initial template. Depending
