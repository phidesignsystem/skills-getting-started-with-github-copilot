import pytest


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister actually removes the participant"""
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Existing participant
        original_count = len(client.get("/activities").json()[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        updated_activities = client.get("/activities").json()

        # Assert
        assert response.status_code == 200
        assert email not in updated_activities[activity_name]["participants"]
        assert len(updated_activities[activity_name]["participants"]) == original_count - 1

    def test_unregister_activity_not_found(self, client, reset_activities):
        """Test unregister for non-existent activity returns 404"""
        # Arrange
        activity_name = "NonExistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_unregister_participant_not_found(self, client, reset_activities):
        """Test unregister for non-existent participant returns 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "notmember@mergington.edu"  # Not signed up

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_unregister_then_signup_again(self, client, reset_activities):
        """Test that a student can signup again after unregistering"""
        # Arrange
        activity_name = "Tennis Club"
        email = "ryan@mergington.edu"

        # Act - unregister
        response1 = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Act - signup again
        response2 = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )
        activities = client.get("/activities").json()

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email in activities[activity_name]["participants"]

    def test_unregister_one_of_many_participants(self, client, reset_activities):
        """Test unregistering one participant doesn't affect others"""
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email_to_remove}"
        )
        activities = client.get("/activities").json()

        # Assert
        assert response.status_code == 200
        assert email_to_remove not in activities[activity_name]["participants"]
        assert email_to_keep in activities[activity_name]["participants"]
