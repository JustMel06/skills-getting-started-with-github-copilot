import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_snapshot


@pytest.fixture(autouse=True)
def reset_activities():
    from src import app as app_module

    app_module.activities = copy.deepcopy(activities_snapshot)
    yield


@pytest.fixture
def client():
    return TestClient(app)
