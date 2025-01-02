import json
from datetime import datetime
from enum import Enum


class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Task:
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, id, description, status=Status.TODO):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID must be a positive integer")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Description must be a non-empty string")

        self.id = id
        self.description = description
        self._status = status
        self._created_at = datetime.now()
        self._updated_at = self._created_at

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    def _update_time(self):
        """Update the updated_at timestamp."""
        self._updated_at = datetime.now()

    @property
    def status(self):
        return self._status

    def updated_status(self, new_status):
        if not isinstance(new_status, Status):
            raise ValueError("new_status must be an instance of Status Enum")
        self._status = new_status
        self._update_time()

    def update_description(self, new_description):
        if not isinstance(new_description, str) or not new_description.strip():
            raise ValueError("new_description must be a non-empty string")
        self.description = new_description
        self._update_time()

    def to_dict(self):
        """Serialising an object into a dictionary for writing to JSON."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.strftime(self.DATETIME_FORMAT),
            "updated_at": self.updated_at.strftime(self.DATETIME_FORMAT),
        }

    def _restore_from_data(self, created_at, updated_at):
        """A private method for recovering temporary attributes from data."""
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def from_dict(cls, data):
        """Deserialising a task from a dictionary when reading JSON."""
        try:
            created_at = datetime.strptime(data["created_at"], cls.DATETIME_FORMAT)
            updated_at = datetime.strptime(data["updated_at"], cls.DATETIME_FORMAT)
            task = cls(
                id=data["id"],
                description=data["description"],
                status=Status(data["status"]),
            )
            task._restore_from_data(created_at, updated_at)
            return task
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid task data: {e}")

    @classmethod
    def formatted_now(cls):
        """Returns the current date and time in the specified format."""
        return datetime.now().strftime(cls.DATETIME_FORMAT)


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = {}
        self.load_from_file()

    def add_task(self, task):
        if task.id in self.tasks:
            raise ValueError(f"Task with id {task.id} already exists")
        self.tasks[task.id] = task
        self.save_to_file()

    def update_task(self, task_id, description=None, status=None):
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        if description:
            task.update_description(description)
        if status:
            task.updated_status(status)
        self.save_to_file()

    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_to_file()
        else:
            raise ValueError(f"Task with id {task_id} not found")

    def list_tasks(self, status=None):
        if status:
            return [task for task in self.tasks.values() if task.status == status]
        return list(self.tasks.values())

    def save_to_file(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks.values()], file, indent=4)

    def load_from_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                self.tasks = {task["id"]: Task.from_dict(task) for task in tasks_data}
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = {}
