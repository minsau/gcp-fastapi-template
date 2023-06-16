include .env

#build core image
build-core:
	@echo "Building core image"
	@docker build -f docker/Dockerfile -t gcr.io/$(GCP_PROJECT_ID)/core --platform linux/amd64 .

push-core:
	@echo "Pushing core image"
	@docker push gcr.io/$(GCP_PROJECT_ID)/core

deploy-core:
	@echo "Deploying core image"
	gcloud run deploy core-service --image gcr.io/$(GCP_PROJECT_ID)/core --platform managed --port 80 --timeout 3600 --concurrency 1 --service-account tickets-hunter-sa@tickets-hunter.iam.gserviceaccount.com --set-env-vars INTERNAL_PORT=80,RUNTYPE=web,PYTHONDONTWRITEBYTECODE=1,USE_GCP=True,GCP_PROJECT_ID=tickets-hunter,GCP_REGION=us-central1,GCP_SECRET_ID=api-config,ENVIRONMENT=production,PROJECT_NAME="Tickets Hunter"

# when you install a package, you will have to run make build to update image
build:
	@docker-compose build

# This will run project and set us up in a bash environment.
up:
	@docker-compose -f docker-compose.yaml up -d
	@docker-compose -f docker-compose.yaml run --service-ports --rm core || true

start:
	@docker-compose -f docker-compose.yaml up -d

reset: #TODO: This is not working
	@docker-compose down
	docker rm -f $(docker ps -a -q)
	docker volume rm $(docker volume ls -q)
