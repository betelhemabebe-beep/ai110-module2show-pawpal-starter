from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    time: str
    duration: int
    priority: str
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner: Owner = owner

    def get_all_tasks(self) -> list[Task]:
        pass

    def sort_tasks_by_time(self) -> list[Task]:
        pass

    def filter_tasks(self, priority: str) -> list[Task]:
        pass

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        pass
