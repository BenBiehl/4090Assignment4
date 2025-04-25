Feature: Todo List Actions

    Scenario: Add a new task
        Given I have no tasks
        When I add a new task called "Do dishes"
        Then the task list should contain "Do dishes"
    
    Scenario: Delete a task
        Given I have a task called "Finish homework"
        When I delete the task "Finish homework"
        Then the task list should not contain the task "Finish homework"

    Scenario: Sort tasks by due date
        Given I have tasks with different due dates
        When I sort tasks by due date
        Then the task with the earliest date should be first

    Scenario: Filter tasks by category
        Given I have tasks in "Work" and "Personal" categories
        When I filter tasks by "Work"
        Then only "Work" tasks should be visible

    Scenario: Mark all tasks as completed
        Given I have a list of incomplete tasks
        When I mark all tasks as complete
        Then the task list should contain only complete tasks
