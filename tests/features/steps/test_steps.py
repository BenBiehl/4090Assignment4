import pytest
import sys
import os
from pytest_bdd import scenarios, given, when, then
from src.tasks import filter_tasks_by_category
from src.tdd import sort_tasks_by_due_date, mark_all_tasks_completed

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' '..' '..')))

scenarios(os.path.abspath("tests/features/tasks.feature"))

@pytest.fixture
def task_list():
    return []

# Add Task
@given("I have no tasks")
def no_tasks(task_list):
    task_list.clear()

@when('I add a new task called "Do dishes"')
def add_dishes(task_list):
    task_list.append({"title": "Do dishes", "completed": False})

@then('the task list should contain "Do dishes"')
def assert_dishes(task_list):
    assert any(task["title"] == "Do dishes" for task in task_list)

# Delete Task
@given('I have a task called "Finish homework"')
def have_homework(task_list):
    task_list.append({"title": "Finish homework", "completed": False})

@when('I delete the task "Finish homework"')
def delete_homework(task_list):
    task_list[:] = [task for task in task_list if task["title"] != "Finish homework"]

@then('the task list should not contain the task "Finish homework"')
def assert_deleted(task_list):
    assert not any(task["title"] == "Finish homework" for task in task_list)

# Sort by Due Date
@given("I have tasks with different due dates")
def tasks_with_due_dates(task_list):
    task_list.extend([
        {"title": "A", "due_date": "2025-04-30"},
        {"title": "B", "due_date": "2025-04-25"}
    ])

@when("I sort tasks by due date")
def sort_due_date(task_list):
    sorted_tasks = sort_tasks_by_due_date(task_list)
    task_list.clear()
    task_list.extend(sorted_tasks)

@then("the task with the earliest date should be first")
def assert_earliest_first(task_list):
    assert task_list[0]["due_date"] == "2025-04-25"

# Filter by Category
@given('I have tasks in "Work" and "Personal" categories')
def categorized_tasks(task_list):
    task_list.extend([
        {"title": "Task 1", "category": "Work"},
        {"title": "Task 2", "category": "Personal"}
    ])

@when('I filter tasks by "Work"')
def filter_work(task_list):
    task_list[:] = filter_tasks_by_category(task_list, "Work")

@then('only "Work" tasks should be visible')
def assert_only_work(task_list):
    assert all(task["category"] == "Work" for task in task_list)

# Mark All as Complete
@given("I have a list of incomplete tasks")
def incomplete_tasks(task_list):
    task_list.extend([
        {"title": "Task A", "completed": False},
        {"title": "Task B", "completed": False}
    ])

@when("I mark all tasks as complete")
def complete_all(task_list):
    updated = mark_all_tasks_completed(task_list)
    task_list.clear()
    task_list.extend(updated)

@then("the task list should contain only complete tasks")
def assert_all_complete(task_list):
    assert all(task["completed"] for task in task_list)