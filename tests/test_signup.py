import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant(self, client, reset_activities):
        """Test that signup actually adds the participant to the activity"""
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"
        original_count = len(client.get("/activities").json()[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )
        updated_activities = client.get("/activities").json()

        # Assert
        assert response.status_code == 200
        assert email in updated_activities[activity_name]["participants"]
        assert len(updated_activities[activity_name]["participants"]) == original_count + 1

    def test_signup_activity_not_found(self, client, reset_activities):
        """Test signup for non-existent activity returns 404"""
        # Arrange
        activity_name = "NonExistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_duplicate_student(self, client, reset_activities):
        """Test that duplicate signup returns 400 error"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_multiple_different_activities(self, client, reset_activities):
        """Test that a student can signup for multiple different activities"""
        # Arrange
        email = "bob@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Tennis Club"

        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )
        activities = client.get("/activities").json()

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_signup_special_characters_in_activity_name(self, client, reset_activities):
        """Test signup with URL-encoded activity name"""
        # Arrange
        activity_name = "Chess Club"
        email = "charlie@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 200
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]
