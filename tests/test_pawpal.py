import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_mark_complete_sets_completed_to_true():
    task = Task(title="Walk", time="08:00", duration=30, priority="high", frequency="daily")

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Luna", species="Dog")
    task = Task(title="Feeding", time="07:00", duration=10, priority="high", frequency="daily")

    assert len(pet.get_tasks()) == 0
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1
