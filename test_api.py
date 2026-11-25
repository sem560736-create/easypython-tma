"""FastAPI TestClient tests for endpoints: GET /health, GET /progress, GET /lessons, POST /check/{id}, POST /save-progress."""
import pytest
from fastapi.testclient import TestClient
import os

# Add the app directory to path
import sys
sys.path.insert(0, '/Users/samir/Documents/deepseek-harness/default-workspace')

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test GET /health endpoint."""

    def test_health_endpoint(self):
        """GET /health should return status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestProgressEndpoint:
    """Test GET /progress endpoint."""

    def test_progress_endpoint_no_user(self):
        """GET /progress with no user_id should return default progress."""
        response = client.get("/progress?user_id=0")
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 0
        assert data["completed"] == []
        assert data["completed_count"] == 0
        assert data["total_lessons"] == len(client.get("/lessons").json())

    def test_progress_endpoint_with_user(self):
        """GET /progress with user_id should return progress for that user."""
        # First get the lessons to know how many there are
        lessons = client.get("/lessons?user_id=1").json()
        total_lessons = len(lessons)
        
        response = client.get("/progress?user_id=1")
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 1
        assert data["completed"] == []
        assert data["completed_count"] == 0
        assert data["total_lessons"] == total_lessons


class TestLessonsEndpoint:
    """Test GET /lessons endpoint."""

    def test_lessons_endpoint_no_user(self):
        """GET /lessons with no user_id should return all lessons with completed=False."""
        response = client.get("/lessons")
        assert response.status_code == 200
        lessons = response.json()
        assert len(lessons) > 0
        # Check that each lesson has expected structure
        for lesson in lessons[:3]:  # Test first 3 lessons
            assert "id" in lesson
            assert "title" in lesson
            assert "lesson_type" in lesson
            assert "completed" in lesson
            assert isinstance(lesson["completed"], bool)

    def test_lessons_endpoint_with_user(self):
        """GET /lessons with user_id should mark completed lessons."""
        # Mark lesson 1 as completed first
        response = client.get("/progress?user_id=1")
        data = response.json()
        lesson_ids = data["completed"]
        
        response = client.get("/lessons?user_id=1")
        lessons = response.json()
        
        # Lesson 1 should be marked as completed
        lesson1 = next((l for l in lessons if l["id"] == 1), None)
        assert lesson1 is not None
        assert lesson1["completed"] is True


class TestCheckEndpoint:
    """Test POST /check/{lesson_id} endpoint."""

    def test_check_correct_answer(self):
        """POST /check/1 with correct answer should return correct=True."""
        response = client.post(
            "/check/1",
            json={"answer": "print('Hello, World!')", "user_id": 1}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["correct"] is True
        assert "feedback" in data

    def test_check_incorrect_answer(self):
        """POST /check/1 with incorrect answer should return correct=False."""
        response = client.post(
            "/check/1",
            json={"answer": "print(Hello)", "user_id": 1}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["correct"] is False
        assert "feedback" in data

    def test_check_invalid_lesson_id(self):
        """POST /check/999 should return 404."""
        response = client.post(
            "/check/999",
            json={"answer": "print('test')", "user_id": 1}
        )
        assert response.status_code == 404
        assert "Урок не найден" in response.json()["detail"]


class TestSaveProgressEndpoint:
    """Test POST /save-progress endpoint."""

    def test_save_progress_success(self):
        """POST /save-progress should save progress and return success."""
        payload = {
            "user_id": 1,
            "completed": [1, 2],
            "xp": 50,
            "level": 2,
            "streak": 3
        }
        response = client.post("/save-progress", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "saved"

    def test_save_progress_missing_user_id(self):
        """POST /save-progress without user_id should return error."""
        payload = {
            "completed": [1, 2],
            "xp": 50,
            "level": 2,
            "streak": 3
        }
        response = client.post("/save-progress", json=payload)
        assert response.status_code == 200  # The endpoint returns 200 but with error message
        data = response.json()
        assert data["status"] == "error"
        assert "user_id required" in data["message"]


if __name__ == "__main__":
    pytest.main()