import pytest
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tdd import mark_all_tasks_completed, sort_tasks_by_due_date, sort_tasks_by_priority

def test_mark_all_tasks_completed():
    tasks = [
        {"id": 1, "title": "One", "completed": False},
        {"id": 2, "title": "Two", "completed": False},
    ]
    updated_tasks = mark_all_tasks_completed(tasks)
    assert all(task["completed"] for task in updated_tasks)

def test_sort_tasks_by_due_date():
    tasks = [
        {"id": 1, "title": "Task A"},
        {"id": 2, "title": "Task B", "due_date": "2025-04-20"},
        {"id": 3, "title": "Task C", "due_date": "2025-04-19"},
    ]
    sorted_tasks = sort_tasks_by_due_date(tasks)
    assert sorted_tasks[0]["id"] == 3 and sorted_tasks[2]["id"] == 1

def test_sort_tasks_by_priority():
    tasks = [
        {"id": 1, "title": "Task A", "priority": "Low"},
        {"id": 2, "title": "Task B", "priority": "High"},
        {"id": 3, "title": "Task C"},
    ]
    sorted_tasks = sort_tasks_by_priority(tasks)
    assert sorted_tasks[0]["id"] == 2