import streamlit as st
import pandas as pd
import subprocess
import sys
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, generate_unique_id

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title:
            new_task = {
                "id": generate_unique_id(tasks), # BUGFIX: Use the function to generate correct ID
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # Display tasks
    for task in filtered_tasks:
        task_col1, task_col2 = st.columns([4, 1]) # BUGFIX: The 'col1' and 'col2' variable names were rused here before
        with task_col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with task_col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    # Tests
    if "test_result" not in st.session_state:
        st.session_state.test_result = ""
    if "test_ran" not in st.session_state:
        st.session_state.test_ran = False

    # Run Tests Button
    if st.sidebar.button("Run Unit Tests"):
        st.sidebar.write("Running tests...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--maxfail=1", "--disable-warnings", "tests/test_basic.py", "--cov=src"],
            capture_output=True,
            text=True
        )
        st.session_state.test_result = result.stdout
        st.session_state.test_ran = True

        if result.returncode != 0:
            st.sidebar.error("Some tests failed.")
        else:
            st.sidebar.success("All tests passed!")

    # Clear Button
    if st.sidebar.button("Clear Test Output"):
        st.session_state.test_result = ""
        st.session_state.test_ran = False

    # Display test output if available
    if st.session_state.test_ran and st.session_state.test_result:
        with st.sidebar.expander("Test Output"):
            st.text(st.session_state.test_result)

if __name__ == "__main__":
    main()