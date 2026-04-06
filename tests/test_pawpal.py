import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


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


def test_sort_tasks_by_time():
    owner = Owner("Betty")
    pet = Pet("Luna", "Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Evening Play", "17:00", 20, "low", "daily"))
    pet.add_task(Task("Morning Walk", "07:00", 30, "high", "daily"))
    pet.add_task(Task("Afternoon Brush", "13:00", 10, "low", "weekly"))
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_tasks_by_time()

    assert sorted_tasks[0].time == "07:00"
    assert sorted_tasks[-1].time == "17:00"


def test_filter_returns_only_pending():
    owner = Owner("Betty")
    pet = Pet("Luna", "Dog")
    owner.add_pet(pet)
    walk = Task("Morning Walk", "07:00", 30, "high", "daily")
    feed = Task("Feeding", "08:00", 10, "high", "daily")
    pet.add_task(walk)
    pet.add_task(feed)
    walk.mark_complete()
    scheduler = Scheduler(owner)

    pending = scheduler.filter_tasks(completed=False)

    assert len(pending) == 1
    assert pending[0].title == "Feeding"


def test_recurring_task_creates_next_occurrence():
    owner = Owner("Betty")
    pet = Pet("Luna", "Dog")
    owner.add_pet(pet)
    walk = Task("Morning Walk", "07:00", 30, "high", "daily", due_date="2026-04-06")
    pet.add_task(walk)
    scheduler = Scheduler(owner)

    scheduler.complete_task(walk)

    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == "2026-04-07"
    assert pet.tasks[1].completed == False


def test_detect_conflict_same_time():
    owner = Owner("Betty")
    pet = Pet("Mochi", "Cat")
    owner.add_pet(pet)
    pet.add_task(Task("Feeding", "08:00", 10, "high", "daily"))
    pet.add_task(Task("Medication", "08:00", 5, "high", "daily"))
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0][0].time == conflicts[0][1].time


def test_no_conflicts_when_no_tasks():
    scheduler = Scheduler(Owner("Betty"))
    assert scheduler.detect_conflicts() == []


def test_one_time_task_does_not_recur():
    owner = Owner("Betty")
    pet = Pet("Luna", "Dog")
    owner.add_pet(pet)
    vet = Task("Vet Visit", "10:00", 60, "high", "once")
    pet.add_task(vet)
    Scheduler(owner).complete_task(vet)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed == True
