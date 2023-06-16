import pytest
import requests
from google.cloud.tasks_v2.services.cloud_tasks.client import CloudTasksClient

from app.core.tasks_manager import TasksManager


@pytest.fixture
def tasks_manager():
    return TasksManager()


def test_create_task_direct_call(mocker, tasks_manager):
    tasks_manager.use_cloud_tasks = False
    mocker.patch.object(requests, "post")
    url = "http://example.com"
    payload = {"key": "value"}
    tasks_manager.create_task(url, payload)
    requests.post.assert_called_once_with(url, json=payload)


def test_create_task_cloud_tasks(mocker, tasks_manager):
    tasks_manager.use_cloud_tasks = True
    mock_create_task = mocker.patch.object(CloudTasksClient, "create_task")
    url = "http://example.com"
    payload = {"key": "value"}
    tasks_manager.create_task(url, payload)
    mock_create_task.assert_called_once()


def test_create_task_cloud_tasks_scheduled(mocker, tasks_manager):
    tasks_manager.use_cloud_tasks = True
    mock_create_task = mocker.patch.object(CloudTasksClient, "create_task")
    url = "http://example.com"
    payload = {"key": "value"}
    in_seconds = 60
    tasks_manager.create_task(url, payload, in_seconds)
    mock_create_task.assert_called_once()
