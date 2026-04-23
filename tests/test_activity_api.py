def test_get_activities_returns_available_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    response = client.get("/activities")
    assert email in response.json()[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 400
    assert first_response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_removes_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    response = client.get("/activities")
    assert email not in response.json()[activity_name]["participants"]


def test_unregister_nonexistent_returns_400(client):
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_activity_not_found_returns_404(client):
    activity_name = "Nonexistent Club"
    email = "someone@mergington.edu"

    post_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert post_response.status_code == 404
    assert post_response.json()["detail"] == "Activity not found"

    delete_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Activity not found"
