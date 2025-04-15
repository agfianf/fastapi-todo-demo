# FastAPI Todo Demo

A simple Todo API built with FastAPI using an in-memory dictionary as storage.

## Features

- CRUD operations for Todo items
- In-memory dictionary storage
- RESTful API endpoints
- Comprehensive test suite

## Requirements

- Python 3.12+
- FastAPI
- Uvicorn (ASGI server)

## Installation

Clone the repository and install dependencies:

```bash
# Install dependencies
pip install -e .

# For development with test dependencies
pip install -e ".[test]"
```

## Running the API

Start the API server with:

```bash
python -m app.main
```

Or using Uvicorn directly:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Root will redirect to the API documentation `/docs`
- `GET /hostname` - Get the hostname of the server
- `POST /todos` - Create a new todo
- `GET /todos` - List all todos
- `GET /todos/{todo_id}` - Get a specific todo
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo

## Running Tests

Run the test suite with:

```bash
pytest
```

## Project Structure

```
fastapi-demo/
├── app/
│   └── main.py       # FastAPI application
├── tests/
│   └── test_main.py  # Tests for the API
├── Dockerfile        # Dockerfile for building the image
├── .gitignore
├── .gitlab-ci.yml    # GitLab CI/CD pipeline configuration
├── pyproject.toml    # Project configuration
├── Makefile          # Makefile for build and test commands
└── README.md         # This file
```