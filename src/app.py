import streamlit as st
import pandas as pd
import subprocess
import sys
import os
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, generate_unique_id
from tdd import mark_all_tasks_completed, sort_tasks_by_due_date, sort_tasks_by_priority

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')
TEST_PATH_BASIC = os.path.join(PROJECT_ROOT, 'tests', 'test_basic.py')
TEST_PATH_TDD = os.path.join(PROJECT_ROOT, 'tests', 'test_tdd.py')
TEST_ADVANCED = os.path.join(PROJECT_ROOT, 'tests', 'test_advanced.py')
TEST_PATH_BDD =  os.path.join(PROJECT_ROOT, 'tests', 'features')
TEST_PATH_PROP = os.path.join(PROJECT_ROOT, 'tests', 'test_property.py')

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

    # New sort task features
    sort_option = st.selectbox("Sort Tasks By", ["Default", "Due Date", "Priority"])
    if sort_option == "Due Date":
        filtered_tasks = sort_tasks_by_due_date(filtered_tasks)
    elif sort_option == "Priority":
        filtered_tasks = sort_tasks_by_priority(filtered_tasks)
    
    # New feature to mark all as complete
    if st.button("Mark All Tasks as Completed"):
        tasks = mark_all_tasks_completed(tasks)
        save_tasks(tasks)
        st.success("All tasks marked as completed.")
        st.rerun()
    
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

    # Tests session state
    st.sidebar.header("Tests")

    if "test_result" not in st.session_state:
        st.session_state.test_result = ""
    if "test_ran" not in st.session_state:
        st.session_state.test_ran = False

    # Run Unit Tests
    if st.sidebar.button("Run Unit Tests"):
        st.sidebar.write("Running unit tests...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--maxfail=1", "--disable-warnings", TEST_PATH_BASIC],
            capture_output=True,
            text=True
        )
        st.session_state.test_result = result.stdout
        st.session_state.test_ran = True

        if result.returncode != 0:
            st.sidebar.error("Some tests failed.")
        else:
            st.sidebar.success("All tests passed!")

    # Run Coverage Test
    if st.sidebar.button("Run Coverage Test"):
        st.sidebar.write("Running coverage tests...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--cov=src", TEST_PATH_BASIC, TEST_ADVANCED, TEST_PATH_TDD, TEST_PATH_PROP],
            capture_output=True,
            text=True
        )
        st.session_state.test_result = result.stdout
        st.session_state.test_ran = True

        if result.returncode != 0:
            st.sidebar.error("Coverage test failed.")
        else:
            st.sidebar.success("Coverage test passed.")

    # Run Parameterized Tests
    if st.sidebar.button("Run Parameterized Test"):
        st.sidebar.write("Running parameterized tests...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", TEST_ADVANCED, "-k", "test_filter_tasks_by_priority"],
            capture_output=True,
            text=True
        )
        st.session_state.test_result = result.stdout
        st.session_state.test_ran = True
        if result.returncode != 0:
            st.sidebar.error("Parameterized test failed.")
        else:
            st.sidebar.success("Parameterized test passed!")

    # Run Mocking Tests
    if st.sidebar.button("Run Mocking Test"):
        st.sidebar.write("Running mocking tests...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", TEST_ADVANCED, "-k", "test_save_tasks_mock"],
            capture_output=True,
            text=True
        )
        st.session_state.test_result = result.stdout
        st.session_state.test_ran = True
        if result.returncode != 0:
            st.sidebar.error("Mocking test failed.")
        else:
            st.sidebar.success("Mocking test passed!")

    # Generate HTML Report
    if st.sidebar.button("Generate HTML Report"):
        st.sidebar.write("Generating HTML report...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", TEST_PATH, "--html=report.html"],
            capture_output=True,
            text=True
        )
        st.session_state.test_result = result.stdout + "\nHTML report saved as report.html"
        st.session_state.test_ran = True
        st.sidebar.success("HTML report generated!")
    
    # Run TDD Tests
    if st.sidebar.button("Run TDD Tests"):
        st.sidebar.write("Running TDD tests...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--maxfail=1", "--disable-warnings", TEST_PATH_TDD],
            capture_output=True,
            text=True
        )
        st.session_state.test_result = result.stdout
        st.session_state.test_ran = True

        if result.returncode != 0:
            st.sidebar.error("Some tests failed.")
        else:
            st.sidebar.success("All tests passed!")

    # Run BDD Tests
    if st.sidebar.button("Run BDD Tests"):
        result = subprocess.run(
            [sys.executable, "-m", "pytest", TEST_PATH_BDD],
            capture_output=True,
            text=True
        )
        st.session_state.test_result = result.stdout
        st.session_state.test_ran = True

        if result.returncode != 0:
            st.sidebar.error("BDD tests failed.")
        else:
            st.sidebar.success("All BDD tests passed.")
    
    # Run Property Tests
    if st.sidebar.button("Run Property Tests"):
        result = subprocess.run(
            [sys.executable, "-m", "pytest", TEST_PATH_PROP],
            capture_output=True,
            text=True
        )
        st.session_state.test_result = result.stdout
        st.session_state.test_ran = True

        if result.returncode != 0:
            st.sidebar.error("Property tests failed.")
        else:
            st.sidebar.success("All property tests passed.")


    # Clear Button
    if st.sidebar.button("Clear Test Output"):
        st.session_state.test_result = ""
        st.session_state.test_ran = False

    # Display Test Output
    if st.session_state.test_ran and st.session_state.test_result:
        with st.sidebar.expander("Test Output"):
            st.text(st.session_state.test_result)


if __name__ == "__main__":
    main()