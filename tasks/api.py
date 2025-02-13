from datetime import date
from typing import List
from ninja import NinjaAPI, Schema
from .models import Task

api = NinjaAPI()

# Schema for Task input
class TaskIn(Schema):
    title: str
    description: str = None
    due_date: date = None
    completed: bool = False

# Schema for Task output
class TaskOut(Schema):
    id: int
    title: str
    description: str = None
    due_date: date = None
    completed: bool

# Create a new task
@api.post("/tasks", response=TaskOut)
def create_task(request, payload: TaskIn):
    task = Task.objects.create(**payload.dict())
    return task

# List all tasks
@api.get("/tasks", response=List[TaskOut])
def list_tasks(request):
    return Task.objects.all()

# Get a single task by ID
@api.get("/tasks/{task_id}", response=TaskOut)
def get_task(request, task_id: int):
    task = Task.objects.get(id=task_id)
    return task

# Update a task
@api.put("/tasks/{task_id}", response=TaskOut)
def update_task(request, task_id: int, payload: TaskIn):
    task = Task.objects.get(id=task_id)
    for attr, value in payload.dict().items():
        setattr(task, attr, value)
    task.save()
    return task

# Delete a task
@api.delete("/tasks/{task_id}")
def delete_task(request, task_id: int):
    task = Task.objects.get(id=task_id)
    task.delete()
    return {"success": True}

# Filter tasks by completion status
@api.get("/tasks/filter/", response=List[TaskOut])
def filter_tasks(request, completed: bool):
    tasks = Task.objects.filter(completed=completed)
    return tasks