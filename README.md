# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

PawPal+ includes lightweight scheduling logic built into the `Scheduler` class:

- **Sorting by time** — `sort_tasks_by_time()` orders all tasks from earliest to latest using each task's `HH:MM` time string, so the daily plan always displays in chronological order.
- **Filtering** — `filter_tasks(completed, pet_name)` lets you view only pending or completed tasks, and optionally narrow results to a single pet by name.
- **Recurring tasks** — When `complete_task()` is called on a daily or weekly task, it automatically creates the next occurrence and adds it to the pet's task list. One-time tasks are simply marked done with nothing added.
- **Conflict detection** — `detect_conflicts()` scans all tasks and returns any pairs scheduled at the same time, so the owner gets a warning before the day begins.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

**What the tests cover:**

- **Sorting** — tasks added out of order are returned in correct chronological order
- **Recurrence** — completing a daily task automatically creates the next occurrence with the correct due date
- **Conflict detection** — two tasks scheduled at the same time are correctly identified as a conflict
- **Filtering** — only tasks matching the requested completion status are returned
- **Edge cases** — no crash when there are no tasks; one-time tasks do not repeat after completion

**Confidence level: ★★★★☆**
Core scheduling behaviors are covered with clear, focused tests. Additional confidence would come from testing the Streamlit UI layer and multi-pet edge cases.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
