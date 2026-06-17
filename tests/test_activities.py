def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    payload = response.json()

    assert response.status_code == 200
    assert len(payload) == 9
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload == {"message": "Signed up new.student@mergington.edu for Chess Club"}


def test_signup_adds_participant_to_activity_state(client):
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    response = client.get("/activities")

    assert "new.student@mergington.edu" in response.json()["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_rejects_missing_activity(client):
    response = client.post(
        "/activities/Robotics Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}