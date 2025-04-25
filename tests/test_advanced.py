import pytest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tasks import filter_tasks_by_priority, save_tasks

# Parameterization Test
@pytest.mark.parametrize("priority, expected_count", [
    ("High", 2),
    ("Medium", 1),
    ("Low", 0)
])
def test_filter_tasks_by_priority(priority, expected_count):
    tasks = [
        {"title": "A", "priority": "High"},
        {"title": "B", "priority": "Medium"},
        {"title": "C", "priority": "High"}
    ]
    filtered = filter_tasks_by_priority(tasks, priority)
    assert len(filtered) == expected_count

# Mocking Test
def test_save_tasks_mock():
    with patch("builtins.open") as mock_open:
        save_tasks([{"title": "Fake Task"}])
        mock_open.assert_called_once()
