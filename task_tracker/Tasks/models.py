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
        self._created_at = self.formatted_now()
        self._updated_at = self._created_at

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    def _update_time(self):
        """Update the updated_at timestamp."""
        self._updated_at = self.formatted_now()

    @property
    def status(self):
        return self._status

    def updated_status(self, new_status):
        if not isinstance(new_status, Status):
            raise ValueError("new_status must be a Status")
        self._status = new_status
        self._update_time()

    def update_description(self, new_description):
        if not isinstance(new_description, str) or not new_description.strip():
            raise ValueError("new_description must be a non-empty string")
        self.description = new_description

    def to_dict(self):
        """Serialising an object into a dictionary for writing to JSON."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
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
