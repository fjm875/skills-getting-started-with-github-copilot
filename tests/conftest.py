from copy import deepcopy

from fastapi.testclient import TestClient
from pytest import fixture

from src.app import activities, app


ORIGINAL_ACTIVITIES = deepcopy(activities)


@fixture()
def client():
    return TestClient(app)


@fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))