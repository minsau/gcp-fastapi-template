# tasks_manager.py
from typing import Dict

import arrow
import requests
from fastapi import HTTPException
from google.cloud import tasks_v2

from app.core.config import settings


class TasksManager:
    def __init__(self):
        self.client = tasks_v2.CloudTasksClient()
        self.project_id = settings.GCP_PROJECT_ID
        self.location_id = settings.GCP_REGION
        self.queue_id = settings.GCP_HIGH_PRIORITY_QUEUE_ID
        self.use_cloud_tasks = settings.USE_CLOUD_TASKS

    def create_task(self, url: str, payload: Dict, in_seconds: int = 0):
        if self.use_cloud_tasks:
            return self._create_cloud_task(url, payload, in_seconds)
        else:
            return self._direct_call(url, payload)

    def _create_cloud_task(self, url: str, payload: Dict, in_seconds: int = 0):
        # Use Google Cloud Tasks to create a task
        parent = self.client.queue_path(self.project_id, self.location_id, self.queue_id)
        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": url,
                "headers": {"Content-Type": "application/json"},
                "body": payload,
            }
        }

        if in_seconds:
            scheduled_time = arrow.utcnow().shift(seconds=in_seconds).isoformat()
            task["schedule_time"] = scheduled_time

        response = self.client.create_task(request={"parent": parent, "task": task})
        return response

    def _direct_call(self, url: str, payload: Dict):
        # Directly call the endpoint in local
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))

        return response
