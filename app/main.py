import os
import platform
import random
import socket
import time
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

# Get version from environment variable, default to "dev" if not set
VERSION = os.environ.get("VERSION", "dev")

app = FastAPI(
    title="Todo API",
    description="A simple Todo API using FastAPI and dictionary storage",
    version=str(VERSION),
)

# In-memory storage for todos
todos: Dict[str, dict] = {}


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = False


class Todo(TodoCreate):
    id: str


class HostInfo(BaseModel):
    hostname: str
    platform: str
    version: str


@app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT, include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get(
    "/system/hostname",
    status_code=status.HTTP_200_OK,
    response_model=HostInfo,
    tags=["system"],
)
async def get_hostname():
    hostname = socket.gethostname()
    system_platform = platform.system()
    print(f"Hostname: {hostname}, Platform: {system_platform}, Version: {VERSION}")
    return {"hostname": hostname, "platform": system_platform, "version": VERSION}


@app.get("/performance/cpu", tags=["performance"])
def cpu_intensive():
    # Simulasi beban CPU
    n = 1_000_000
    for _ in range(n):
        random.random()
    return {"status": "completed"}


@app.get("/performance/memory", tags=["performance"])
def memory_intensive():
    # Simulasi beban memory
    large_list = [i for i in range(1_000_000)]
    time.sleep(0.1)
    return {"status": "completed", "size": len(large_list)}


@app.post(
    "/todos",
    status_code=status.HTTP_201_CREATED,
    response_model=Todo,
    tags=["todos"],
)
async def create_todo(todo: TodoCreate):
    todo_id = str(uuid4())
    todo_dict = todo.model_dump()
    todo_dict["id"] = todo_id
    todos[todo_id] = todo_dict
    return todo_dict


@app.get(
    "/todos",
    status_code=status.HTTP_200_OK,
    response_model=List[Todo],
    tags=["todos"],
)
async def get_todos():
    return list(todos.values())


@app.get(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=Todo,
    tags=["todos"],
)
async def get_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )
    return todos[todo_id]


@app.put(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=Todo,
    tags=["todos"],
)
async def update_todo(todo_id: str, todo: TodoCreate):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    todo_dict = todo.model_dump()
    todo_dict["id"] = todo_id
    todos[todo_id] = todo_dict
    return todo_dict


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["todos"])
async def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )

    del todos[todo_id]
    return None


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
