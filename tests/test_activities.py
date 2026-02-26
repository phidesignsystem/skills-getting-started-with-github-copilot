import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_success(self, client, reset_activities):
        """Test that GET /activities returns all activities with 200 status"""
        # Arrange
        expected_activity_count = 9

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities

    def test_get_activities_structure(self, client, reset_activities):
        """Test that each activity has the correct structure"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_participants_loaded(self, client, reset_activities):
        """Test that activities have pre-loaded participants"""
        # Arrange
        expected_chess_club_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert set(chess_club["participants"]) == set(expected_chess_club_participants)
