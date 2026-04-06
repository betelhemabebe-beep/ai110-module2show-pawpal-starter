from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner(name="Betty")

# Create pets
luna = Pet(name="Luna", species="Dog")
mochi = Pet(name="Mochi", species="Cat")

# Add pets to owner
owner.add_pet(luna)
owner.add_pet(mochi)

# Add tasks — two intentionally share the same time to trigger conflict detection
evening_play = Task(title="Evening Playtime", time="17:00", duration=20, priority="medium", frequency="daily")
feeding = Task(title="Feeding", time="08:00", duration=10, priority="high", frequency="daily")
medication = Task(title="Medication", time="08:00", duration=5, priority="high", frequency="daily")  # same time as Feeding
morning_walk = Task(title="Morning Walk", time="07:00", duration=30, priority="high", frequency="daily")
afternoon_brush = Task(title="Brush Fur", time="13:00", duration=10, priority="low", frequency="weekly")

# Mark one task as completed to test filtering
morning_walk.mark_complete()

# Add tasks to pets
luna.add_task(evening_play)
luna.add_task(feeding)
luna.add_task(morning_walk)
mochi.add_task(medication)
mochi.add_task(afternoon_brush)

# Create scheduler
scheduler = Scheduler(owner=owner)

# --- Sort by Time ---
print("=" * 42)
print(f"  PawPal+ | {owner.name}'s Schedule (Sorted)")
print("=" * 42)

sorted_tasks = scheduler.sort_tasks_by_time()
for task in sorted_tasks:
    status = "Done   " if task.completed else "Pending"
    print(f"  {task.time}  |  {task.title:<20} [{status}]")
    print(f"           Duration: {task.duration} min | Priority: {task.priority}")
    print()

# --- Filter: Pending Tasks ---
print("=" * 42)
print("  Pending Tasks (not yet completed)")
print("=" * 42)

pending = scheduler.filter_tasks(completed=False)
if pending:
    for task in pending:
        print(f"  - {task.title} at {task.time}")
else:
    print("  All tasks are complete!")
print()

# --- Filter: Completed Tasks ---
print("=" * 42)
print("  Completed Tasks")
print("=" * 42)

done = scheduler.filter_tasks(completed=True)
if done:
    for task in done:
        print(f"  - {task.title} at {task.time}")
else:
    print("  No tasks completed yet.")
print()

# --- Filter: Tasks for a Specific Pet ---
print("=" * 42)
print("  Luna's Pending Tasks")
print("=" * 42)

luna_pending = scheduler.filter_tasks(completed=False, pet_name="Luna")
if luna_pending:
    for task in luna_pending:
        print(f"  - {task.title} at {task.time}")
else:
    print("  Luna has no pending tasks.")
print()

# --- Conflict Detection ---
print("=" * 42)
print("  Conflict Check")
print("=" * 42)

conflicts = scheduler.detect_conflicts()
if conflicts:
    print("  WARNING: Scheduling conflicts found!")
    print()
    for task_a, task_b in conflicts:
        print(f"  - '{task_a.title}' and '{task_b.title}' are both scheduled at {task_a.time}")
else:
    print("  No scheduling conflicts found.")

print("=" * 42)
