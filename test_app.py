import pytest
from app import app, notes


@pytest.fixture
def client():
    """Creates a test client and clears data before each test."""
    app.config["TESTING"] = True
    notes.clear()  # reset in-memory data before every test runs
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test 1: GET /health returns status ok with a 200 code."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_and_get_note(client):
    """Test 2: POST /notes creates a note, and GET /notes retrieves it."""
    # Create note
    post_res = client.post("/notes", json={"id": 101, "text": "Testing with Pytest"})
    assert post_res.status_code == 201

    # Get notes and verify
    get_res = client.get("/notes")
    assert get_res.status_code == 200
    assert get_res.get_json() == [{"id": 101, "text": "Testing with Pytest"}]


def test_delete_note(client):
    """Test 3: DELETE /notes/<id> removes the note successfully."""
    # First add a note
    client.post("/notes", json={"id": 202, "text": "Note to delete"})

    # Delete it
    del_res = client.delete("/notes/202")
    assert del_res.status_code == 200

    # Ensure it's gone
    get_res = client.get("/notes")
    assert get_res.get_json() == []


def test_delete_nonexistent_note(client):
    """Test 4: DELETE a note that doesn't exist should return 404."""
    del_res = client.delete("/notes/9999")
    assert del_res.status_code == 404
    assert del_res.get_json() == {"error": "Note not found"}