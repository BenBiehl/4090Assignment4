import pytest
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tasks import (
    load_tasks,
    save_tasks,
    generate_unique_id,
    filter_tasks_by_category,
    filter_tasks_by_priority,
    filter_tasks_by_completion,
    search_tasks,
    get_overdue_tasks
)

TEST_FILE = "test_file.json"

@pytest.fixture
def test_tasks():
    return [
        {"id": 1, "title": "Test 1", "priority": "High", "category": "Work", "completed": False, "due_date": "2025-04-19"},
        {"id": 2, "title": "Test 2", "priority": "Low", "category": "Personal", "completed": True, "due_date": "2025-04-23"},
    ]

# Test to ensure saving and loading tasks work
def test_save_and_load(test_tasks):
    save_tasks(test_tasks, TEST_FILE)
    loaded = load_tasks(TEST_FILE)
    assert loaded == test_tasks
    os.remove(TEST_FILE)

# Test to make sure correct ID is generated
def test_generate_id(test_tasks):
    uid = generate_unique_id(test_tasks)
    assert uid == 3

# Test to make sure filtering works
def test_filter(test_tasks):
    filtered_priority = filter_tasks_by_priority(test_tasks, "High")
    filtered_category = filter_tasks_by_category(test_tasks, "Personal")
    filtered_completion = filter_tasks_by_completion(test_tasks, True)
    assert len(filtered_priority) == 1
    assert filtered_priority[0]["title"] == "Test 1"
    assert len(filtered_category) == 1
    assert filtered_category[0]["title"] == "Test 2"
    assert len(filtered_completion) == 1
    assert filtered_completion[0]["title"] == "Test 2"

# Test to ensure searching works
def test_search(test_tasks):
    result = search_tasks(test_tasks, "Test 1")
    assert len(result) == 1
    assert result[0]["id"] == 1

# Test to ensre that overdue tasks are correctly detected
def test_overdue(test_tasks):
    overdue = get_overdue_tasks(test_tasks)
    assert len(overdue) == 1
    assert overdue[0]["id"] == 1

# Test to make sure non-existent json file is handled correctly
def test_nonexistent_json():
    with open(TEST_FILE, "w") as f:
        f.write("{ invalid json }")
    result = load_tasks(TEST_FILE)
    assert result == []
    os.remove(TEST_FILE)