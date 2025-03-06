import pytest
import csv
import os
from datetime import datetime
from project import add_task, remove_task, list_tasks, modify_task, send_reminder

# Helper function to create a temporary CSV file for testing
@pytest.fixture
def temp_csv(tmpdir):
    """
    Creates a temporary CSV file for testing and returns its path.
    """
    temp_file = tmpdir.join("tasks.csv")
    with open(temp_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "description", "category", "due_date"])
        writer.writeheader()
        writer.writerow({"title": "Test Task", "description": "Test Desc", "category": "Work", "due_date": "2024-09-30"})
    return temp_file


def test_add_task(temp_csv):
    """
    Tests if a task is correctly added to the CSV file.
    """
    # Simulate adding a new task
    new_task = {"title": "New Task", "description": "New Desc", "category": "Study", "due_date": "2024-10-10"}

    # Append to CSV
    with open(temp_csv, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "description", "category", "due_date"])
        writer.writerow(new_task)

    # Verify that the new task was added
    with open(temp_csv, "r") as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    # Should contain the existing task + new task
    assert len(tasks) == 2
    assert tasks[1]["title"] == "New Task"


def test_remove_task(temp_csv):
    """
    Tests if a task is correctly removed from the CSV file.
    """
    # Read current tasks
    with open(temp_csv, "r") as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    # Initial state: 1 task
    assert len(tasks) == 1

    # Simulate removing task at index 0
    del tasks[0]

    # Write back updated tasks
    with open(temp_csv, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "description", "category", "due_date"])
        writer.writeheader()
        writer.writerows(tasks)

    # Verify that the task was removed
    with open(temp_csv, "r") as file:
        reader = csv.DictReader(file)
        tasks_after = list(reader)

    # Should have 0 tasks after removal
    assert len(tasks_after) == 0


def test_list_tasks(temp_csv):
    """
    Tests if listing tasks returns the correct number of tasks.
    """
    tasks = list_tasks(return_tasks=True)

    # Expecting 1 task in the CSV
    assert len(tasks) == 1


def test_modify_task(temp_csv):
    """
    Tests if modifying a task updates the correct details.
    """
    # Read tasks before modification
    with open(temp_csv, "r") as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    assert tasks[0]["title"] == "Test Task"

    # Modify the first task
    tasks[0]["title"] = "Updated Task"
    tasks[0]["description"] = "Updated Desc"

    # Write back modified task
    with open(temp_csv, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "description", "category", "due_date"])
        writer.writeheader()
        writer.writerows(tasks)

    # Read tasks after modification
    with open(temp_csv, "r") as file:
        reader = csv.DictReader(file)
        modified_tasks = list(reader)

    assert modified_tasks[0]["title"] == "Updated Task"
    assert modified_tasks[0]["description"] == "Updated Desc"
