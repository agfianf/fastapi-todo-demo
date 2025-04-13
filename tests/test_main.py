import pytest
from fastapi.testclient import TestClient
from app.main import app, todos

client = TestClient(app)

@pytest.fixture
def clear_todos():
    # Clear todos before each test
    todos.clear()
    yield
    # Clear todos after each test
    todos.clear()


# def test_root_endpoint():
#     response = client.get("/")
#     print(f"Response: {response.status_code}, Headers: {response.headers}")
#     assert response.status_code == 307
#     assert response.headers["location"] == "/docs"


def test_create_todo(clear_todos):
    # Test creating a todo
    todo_data = {"title": "Test Todo", "description": "This is a test", "completed": False}
    response = client.post("/todos", json=todo_data)
    assert response.status_code == 201
    response_json = response.json()
    assert "id" in response_json
    assert response_json["title"] == todo_data["title"]
    assert response_json["description"] == todo_data["description"]
    assert response_json["completed"] == todo_data["completed"]


def test_get_todos(clear_todos):
    # Create a few todos first
    todo1 = {"title": "Todo 1", "description": "First todo"}
    todo2 = {"title": "Todo 2", "description": "Second todo", "completed": True}
    
    response1 = client.post("/todos", json=todo1)
    response2 = client.post("/todos", json=todo2)
    
    # Test getting all todos
    response = client.get("/todos")
    assert response.status_code == 200
    todos_list = response.json()
    assert len(todos_list) == 2


def test_get_single_todo(clear_todos):
    # Create a todo
    todo_data = {"title": "Get Test", "description": "Testing get single"}
    response = client.post("/todos", json=todo_data)
    todo_id = response.json()["id"]
    
    # Get the created todo
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["title"] == todo_data["title"]
    
    # Try to get a non-existent todo
    response = client.get("/todos/nonexistent-id")
    assert response.status_code == 404


def test_update_todo(clear_todos):
    # Create a todo
    todo_data = {"title": "Old Title", "description": "Old description"}
    response = client.post("/todos", json=todo_data)
    todo_id = response.json()["id"]
    
    # Update the todo
    updated_data = {"title": "New Title", "description": "New description", "completed": True}
    response = client.put(f"/todos/{todo_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]
    assert response.json()["completed"] == updated_data["completed"]
    
    # Try to update a non-existent todo
    response = client.put("/todos/nonexistent-id", json=updated_data)
    assert response.status_code == 404


def test_delete_todo(clear_todos):
    # Create a todo
    todo_data = {"title": "Delete Me", "description": "To be deleted"}
    response = client.post("/todos", json=todo_data)
    todo_id = response.json()["id"]
    
    # Verify todo exists
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    
    # Delete the todo
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    
    # Verify todo is gone
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404
    
    # Try to delete a non-existent todo
    response = client.delete("/todos/nonexistent-id")
    assert response.status_code == 404