import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Create a default Owner once and keep it alive across Streamlit reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="My Owner")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    # Check for duplicate pet names before adding
    existing_names = [p.name for p in st.session_state.owner.pets]
    if pet_name in existing_names:
        st.warning(f"{pet_name} is already added.")
    else:
        new_pet = Pet(name=pet_name, species=species)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"{pet_name} the {species} added!")

# --- Add a Task ---
st.subheader("Add a Task")

# Build a list of pet names to choose from
pet_names = [p.name for p in st.session_state.owner.pets]

if pet_names:
    selected_pet_name = st.selectbox("Assign task to pet", pet_names)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        # Find the selected pet object and add the task to it
        for pet in st.session_state.owner.pets:
            if pet.name == selected_pet_name:
                new_task = Task(
                    title=task_title,
                    time=task_time,
                    duration=int(duration),
                    priority=priority,
                    frequency="daily",
                )
                pet.add_task(new_task)
                st.success(f"Task '{task_title}' added to {pet.name}!")
                break
else:
    st.info("Add a pet first before adding tasks.")

# --- Display Sorted Schedule ---
st.divider()
st.subheader("Today's Schedule")

if st.session_state.owner.pets:
    scheduler = Scheduler(owner=st.session_state.owner)
    sorted_tasks = scheduler.sort_tasks_by_time()

    if sorted_tasks:
        # Build a list of dicts for st.table
        rows = []
        for task in sorted_tasks:
            rows.append({
                "Time": task.time,
                "Task": task.title,
                "Duration (min)": task.duration,
                "Priority": task.priority,
                "Status": "Done" if task.completed else "Pending",
            })
        st.table(rows)

        # Show a warning if any tasks conflict
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for task_a, task_b in conflicts:
                st.warning(f"Scheduling conflict: '{task_a.title}' and '{task_b.title}' are both at {task_a.time}")
    else:
        st.info("No tasks yet. Add tasks above to see your schedule.")
else:
    st.info("No pets added yet.")
