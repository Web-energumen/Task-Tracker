import argparse

from prettytable import PrettyTable

from Tasks.models import Status, Task, TaskManager


class CLIApp:
    def __init__(self):
        self.task_manager = TaskManager()

    def run(self):
        parser = argparse.ArgumentParser(description="Task Management Application")

        subparsers = parser.add_subparsers(dest="subcommand", required=True)

        # Add a task
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("id", type=int, help="Task ID (positive integer)")
        add_parser.add_argument("description", type=str, help="Task description")

        # Update a task
        update_parser = subparsers.add_parser("update", help="Update a task")
        update_parser.add_argument("id", type=int, help="Task ID")
        update_parser.add_argument("--description", type=str, help="New task description")
        update_parser.add_argument("--status", type=str, choices=[s.value for s in Status],
                                   help="New task status (todo, in-progress, done)")

        # Delete a task
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("id", type=int, help="Task ID")

        # List tasks
        list_parser = subparsers.add_parser("list", help="List tasks")
        list_parser.add_argument("--status", type=str, choices=[s.value for s in Status],
                                 help="Filter tasks by status")

        args = parser.parse_args()
        self.handle_command(args)

    def handle_command(self, args):
        try:
            if args.subcommand == "add":
                self.task_manager.add_task(Task(id=args.id, description=args.description))
                print(f"Task {args.id} added successfully.")

            elif args.subcommand == "update":
                status = Status(args.status) if args.status else None
                self.task_manager.update_task(args.id, description=args.description, status=status)
                print(f"Task {args.id} updated successfully.")

            elif args.subcommand == "delete":
                self.task_manager.delete_task(args.id)
                print(f"Task {args.id} deleted successfully.")

            elif args.subcommand == "list":
                tasks = (self.task_manager.list_tasks(status=Status(args.status))
                         if args.status else self.task_manager.list_tasks())
                if tasks:
                    self.print_tasks_as_table(tasks)
                else:
                    print("No tasks found.")
        except Exception as e:
            print(f"Error: {e}")

    def print_tasks_as_table(self, tasks):
        """Prints tasks in a table format."""
        table = PrettyTable()
        table.field_names = ["ID", "Description", "Status", "Created At", "Updated At"]
        for task in tasks:
            table.add_row([task.id, task.description, task.status.value, task.created_at, task.updated_at])
        print(table)
