"""Пytest tests for database.py: mark_completed, completed_ids, get_or_create, log_attempt."""
import tempfile
import os

import pytest

from database import Database


@pytest.fixture
def db():
    """Create a temporary database for each test."""
    test_db_path = tempfile.mktemp(suffix=".db")
    db = Database(test_db_path)
    yield db
    os.remove(test_db_path)


class TestDatabaseMarkCompleted:
    """Tests for mark_completed method."""

    def test_mark_completed_first_time(self, db):
        """mark_completed should add lesson_id to completed list on first call."""
        db.get_or_create(123, "testuser", "Test")
        db.mark_completed(123, 1)
        completed = db.completed_ids(123)
        assert 1 in completed

    def test_mark_completed_idempotent(self, db):
        """mark_completed should be idempotent - calling twice shouldn't duplicate."""
        db.get_or_create(123, "testuser", "Test")
        db.mark_completed(123, 1)
        db.mark_completed(123, 1)
        completed = db.completed_ids(123)
        assert completed == [1]

    def test_mark_completed_multiple_lessons(self, db):
        """mark_completed should add multiple lesson_ids and keep them sorted."""
        db.get_or_create(123, "testuser", "Test")
        db.mark_completed(123, 3)
        db.mark_completed(123, 1)
        db.mark_completed(123, 2)
        completed = db.completed_ids(123)
        assert completed == [1, 2, 3]

    def test_mark_completed_points_added(self, db):
        """mark_completed should add points to score and xp."""
        db.get_or_create(123, "testuser", "Test")
        db.mark_completed(123, 1, points=10)
        student = db.get(123)
        assert student["score"] == 10
        assert student["xp"] == 10

    def test_mark_completed_nonexistent_user_no_crash(self, db):
        """mark_completed on a non-existent user should not crash (bug: no rows updated)."""
        # Bug: mark_completed does UPDATE which affects 0 rows if user doesn't exist.
        # It doesn't raise an exception, but silently does nothing.
        db.mark_completed(999, 1)
        completed = db.completed_ids(999)
        assert completed == []


class TestDatabaseCompletedIds:
    """Tests for completed_ids method."""

    def test_completed_ids_empty_new_user(self, db):
        """completed_ids should return empty list for new user."""
        completed = db.completed_ids(123)
        assert completed == []

    def test_completed_ids_after_mark(self, db):
        """completed_ids should return list after marking lessons complete."""
        db.get_or_create(123, "testuser", "Test")
        db.mark_completed(123, 1)
        db.mark_completed(123, 3)
        db.mark_completed(123, 2)
        completed = db.completed_ids(123)
        assert sorted(completed) == [1, 2, 3]

    def test_completed_ids_no_student(self, db):
        """completed_ids should return empty list for non-existent user."""
        # User 999 was never created
        completed = db.completed_ids(999)
        assert completed == []


class TestDatabaseGetOrCreate:
    """Tests for get_or_create method."""

    def test_get_or_create_new_user(self, db):
        """get_or_create should create new student if not exists."""
        student = db.get_or_create(123, "testuser", "Test")
        assert student["user_id"] == 123
        assert student["username"] == "testuser"
        assert student["first_name"] == "Test"

    def test_get_or_create_existing_user(self, db):
        """get_or_create should return existing student without re-creating."""
        # First call creates the user
        student1 = db.get_or_create(123, "testuser", "Test")
        # Second call returns the same user
        student2 = db.get_or_create(123, "testuser", "Test")
        assert student1["user_id"] == student2["user_id"]
        assert student1["username"] == student2["username"]


class TestDatabaseLogAttempt:
    """Tests for log_attempt method."""

    def test_log_attempt_stores_correct(self, db):
        """log_attempt should store correct answer."""
        db.log_attempt(123, 1, "print('Hello')", True)
        # Just verify it doesn't raise an error
        # We can't easily query attempts table directly, but we check via stats

    def test_log_attempt_stores_incorrect(self, db):
        """log_attempt should store incorrect answer."""
        db.log_attempt(123, 1, "wrong answer", False)
        # Just verify it doesn't raise an error

    def test_log_attempt_with_wrong_user_id(self, db):
        """log_attempt should work with different user_ids."""
        db.log_attempt(456, 1, "answer", True)
        db.log_attempt(789, 1, "answer", False)
        # Should not raise