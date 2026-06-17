def test_remove_participant_removes_existing_student(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload == {"message": "Removed michael@mergington.edu from Chess Club"}


def test_remove_participant_updates_activity_state(client):
    client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    response = client.get("/activities")

    assert "michael@mergington.edu" not in response.json()["Chess Club"]["participants"]


def test_remove_participant_rejects_missing_activity(client):
    response = client.delete(
        "/activities/Robotics Club/participants",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_remove_participant_rejects_missing_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "missing.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}