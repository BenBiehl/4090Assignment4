from hypothesis import given
from hypothesis.strategies import text, dates, lists, booleans, sampled_from, integers
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tdd import sort_tasks_by_due_date, mark_all_tasks_completed
from tasks import filter_tasks_by_category, generate_unique_id

@given(title=text(min_size=1, max_size=100))
def test_adding_task_preserves_title(title):
    tasks = []
    task = {"title": title, "completed": False}
    tasks.append(task)

    assert tasks[-1]["title"] == title
    assert not tasks[-1]["completed"]

@given(dates_list=lists(dates(), min_size=2))
def test_due_date_sorting(dates_list):
    tasks = [{"title": str(i), "due_date": str(date), "completed": False} for i, date in enumerate(dates_list)]
    sorted_tasks = sort_tasks_by_due_date(tasks)
    sorted_dates = [task["due_date"] for task in sorted_tasks]
    assert sorted_dates == sorted(sorted_dates)

@given(completed_list=lists(booleans(), min_size=1))
def test_mark_all_tasks_completed(completed_list):
    tasks = [{"title": f"Task {i}", "completed": status} for i, status in enumerate(completed_list)]
    updated = mark_all_tasks_completed(tasks)
    assert all(task["completed"] for task in updated)

@given(categories=lists(sampled_from(["Work", "Personal", "Other"]), min_size=1))
def test_filter_by_category(categories):
    tasks = [{"title": f"Task {i}", "category": cat} for i, cat in enumerate(categories)]
    target = categories[0]
    filtered = filter_tasks_by_category(tasks, target)
    assert all(task["category"] == target for task in filtered)

@given(lists(integers(min_value=1, max_value=1000)))
def test_generate_unique_id(tasks):
    task_list = [{"id": task} for task in tasks]
    unique_id = generate_unique_id(task_list)
    if task_list:
        max_id = max(task["id"] for task in task_list)
        assert unique_id > max_id
    else:
        assert unique_id == 1