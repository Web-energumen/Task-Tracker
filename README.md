# Task Tracker CLI

## Project Overview
Python sample solution for the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh/).

This is a simple command-line interface (CLI) tool that allows users to track and manage their tasks efficiently. The application provides functionality to add, update, delete, and list tasks with different statuses: todo, in-progress, and done. Tasks are persisted in a local JSON file, enabling offline access and lightweight usage without any external dependencies.

This project is a great exercise to practice core programming skills including CLI argument handling, JSON file manipulation, and basic project structure in Python.

## Features
* Add Tasks: Add a new task with a description.
* Update Tasks: Modify the description of an existing task.
* Delete Tasks: Remove a task by its ID.
* Mark Tasks:
  - As In Progress
  - As Done
* List Tasks:
  - All tasks
  - Tasks by status (todo, in-progress, done)
* Persistent Storage: All tasks are stored in a tasks.json file in the project directory.
* Error Handling: Handles non-existent IDs, invalid inputs.

## Technologies Used
* Python 3: Core programming language.
* argparse: To handle CLI commands and arguments.
* JSON module: For reading/writing tasks to a local file.
* os & datetime: For file management and timestamps.
* PrettyTable: For displaying tasks in tabular format

## Installation
### Prerequisites
* Python 3.10+

### Steps
1. Clone the Repository:
```bash
 git clone https://github.com/Web-energumen/Task-Tracker.git 
 cd Task-Tracker/task_tracker
```

2. Set Up Virtual Environment:
```bash
 python3 -m venv venv
 source venv/bin/activate
```

3. Install Dependencies:
```
pip install -r requirements.txt
```

## Usage
### Add a Task
```
python main.py add 3 "Finish homework"
```

### Update a Task
```
python main.py update 3 --description "Finish math and science homework
```

### Delete a Task
```
python main.py delete 1
```

### Mark Task as done 
```
python main.py update 3 --status done
```

### List Tasks
```
python main.py list                       # All tasks
python main.py list --status todo         # Only todo
python main.py list --status in-progress  # Only in progress
python main.py list --status done         # Only Done
```

## Example
```
python main.py add 4 "Write blog post"
Task 4 added successfully.

python main.py update 4 --status in-progress
Task 4 updated successfully

python main.py list
+----+----------------------------------+-------------+---------------------+---------------------+
| ID |           Description            |    Status   |      Created At     |      Updated At     |
+----+----------------------------------+-------------+---------------------+---------------------+
| 2  |       Updated description        | in-progress | 2024-12-06 12:41:33 | 2024-12-06 12:41:47 |
| 3  | Finish math and science homework |     done    | 2025-04-10 13:53:04 | 2025-04-10 14:03:37 |
| 4  |         Write blog post          | in-progress | 2025-04-10 14:10:09 | 2025-04-10 14:11:10 |
+----+----------------------------------+-------------+---------------------+---------------------+
```
