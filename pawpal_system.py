from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    """Represents a single care task assigned to a pet."""

    title: str
    time: str
    duration: int
    priority: str
    frequency: str
    completed: bool = False
    due_date: str = field(default_factory=lambda: date.today().isoformat())

    def mark_complete(self) -> "Task | None":
        """Mark this task done and return a new task for the next due date if it recurs."""
        self.completed = True
        if self.frequency in ("daily", "weekly"):
            current = date.fromisoformat(self.due_date)
            if self.frequency == "daily":
                next_date = current + timedelta(days=1)
            else:
                next_date = current + timedelta(weeks=1)
            return Task(
                title=self.title,
                time=self.time,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency,
                due_date=next_date.isoformat(),
            )
        return None  # one-time task, no follow-up needed


@dataclass
class Pet:
    """Represents a pet owned by the owner."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


class Owner:
    """Represents the pet owner who manages one or more pets."""

    def __init__(self, name: str) -> None:
        """Initialize the owner with a name and an empty list of pets."""
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across every pet the owner has."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Scheduler:
    """Organizes and manages tasks for all of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""
        self.owner: Owner = owner

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_tasks_by_time(self) -> list[Task]:
        """Sort all tasks from earliest to latest using the HH:MM time string."""
        return sorted(self.get_all_tasks(), key=lambda task: (int(task.time.split(":")[0]), int(task.time.split(":")[1])))

    def sort_tasks_by_priority(self) -> list[Task]:
        """Sort all tasks by priority level: high first, then medium, then low."""
        return sorted(self.get_all_tasks(), key=lambda t: _PRIORITY_ORDER.get(t.priority, 3))

    def filter_tasks(self, completed: bool, pet_name: str = None) -> list[Task]:
        """Return tasks matching the given completion status, optionally limited to one pet."""
        if pet_name is not None:
            tasks = []
            for pet in self.owner.pets:
                if pet.name.lower() == pet_name.lower():
                    tasks = pet.get_tasks()
                    break
        else:
            tasks = self.get_all_tasks()
        return [task for task in tasks if task.completed == completed]

    def complete_task(self, task: Task) -> None:
        """Mark a task done and add the next occurrence to its pet if it repeats daily or weekly."""
        next_task = task.mark_complete()
        if next_task is not None:
            for pet in self.owner.pets:
                if task in pet.tasks:
                    pet.add_task(next_task)
                    break

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return every pair of tasks that share the same scheduled time."""
        tasks = self.get_all_tasks()
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].time == tasks[j].time:
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts
