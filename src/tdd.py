import json
import os
from datetime import datetime

# File path for task storage
DEFAULT_TASKS_FILE = "tasks.json"

def mark_all_tasks_completed(tasks):
    """
    Take in a list of tasks and mark them all as complete.
    
    Args:
        tasks (list): List of existing task dictionaries
        
    Returns:
        list: list of tasks all marked as complete
    """
    for task in tasks:
        task["completed"] = True
    return tasks

def sort_tasks_by_due_date(tasks):
    """
    Sort a list of tasks by their due date, with tasks having no due date placed last.
    
    Args:
        tasks (list): List of existing task dictionaries
        
    Returns:
        list: List of tasks sorted by their due date, tasks with no due date placed last
    """
    return sorted(tasks, key=lambda x: x.get("due_date", "9999-12-31"))

def sort_tasks_by_priority(tasks):
    """
    Sort a list of tasks by their priority (High, Medium, Low).
    
    Args:
        tasks (list): List of existing task dictionaries
        
    Returns:
        list: List of tasks sorted by their priority
    """
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    return sorted(tasks, key=lambda x: priority_order.get(x.get("priority", "Low"), 3))