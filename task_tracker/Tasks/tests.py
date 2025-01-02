import json
import os
import unittest
from datetime import datetime

from Tasks.models import Status, Task, TaskManager


class TestTasks(unittest.TestCase):
    def test_task_initialisation(self):
        task = Task(id=1, description="Test Task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Test Task")
        self.assertEqual(task.status, Status.TODO)
        self.assertIsInstance(task.created_at, datetime)
        self.assertIsInstance(task.updated_at, datetime)

    def test_update_status(self):
        task = Task(id=1, description="Test Task")
        task.updated_status(Status.IN_PROGRESS)
        self.assertEqual(task.status, Status.IN_PROGRESS)

    def test_update_description(self):
        task = Task(id=1, description="Test Task")
        task.update_description("Test Description")
        self.assertEqual(task.description, "Test Description")

    def test_to_dict(self):
        task = Task(id=1, description="Test Task")
        task_dict = task.to_dict()
        self.assertIsInstance(task_dict, dict)
        self.assertEqual(task_dict["id"], 1)
        self.assertEqual(task_dict["description"], "Test Task")
        self.assertEqual(task_dict["status"], "todo")

    def test_from_dict(self):
        task_data = {
            "id": 1,
            "description": "Test Task",
            "status": "todo",
            "created_at": "2024-12-08 10:00:00",
            "updated_at": "2024-12-08 12:00:00"
        }
        task = Task.from_dict(task_data)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Test Task")
        self.assertEqual(task.status, "todo")


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.json"
        self.task_manager = TaskManager(filename=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        task = Task(id=1, description="Test Task")
        self.task_manager.add_task(task)
        self.assertIn(1, self.task_manager.tasks)
        self.assertEqual(self.task_manager.tasks[1].description,"Test Task")

    def test_update_task(self):
        task = Task(id=1, description="Test Task")
        self.task_manager.add_task(task)
        self.task_manager.update_task(1, description="Test Description", status=Status.DONE)
        self.assertEqual(self.task_manager.tasks[1].description, "Test Description")
        self.assertEqual(self.task_manager.tasks[1].status, Status.DONE)

    def test_delete_task(self):
        task = Task(id=1, description="Test Task")
        self.task_manager.add_task(task)
        self.task_manager.delete_task(1)
        self.assertNotIn(1, self.task_manager.tasks)

    def test_list_tasks(self):
        task1 = Task(id=1, description="Test Task 1", status=Status.TODO)
        task2 = Task(id=2, description="Test Task 2", status=Status.DONE)
        self.task_manager.add_task(task1)
        self.task_manager.add_task(task2)

        todo_tasks = self.task_manager.list_tasks(status=Status.TODO)
        done_tasks = self.task_manager.list_tasks(status=Status.DONE)

        self.assertEqual(len(todo_tasks), 1)
        self.assertEqual(todo_tasks[0].description, "Test Task 1")
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0].description, "Test Task 2")

    def test_save_and_load_from_file(self):
        task = Task(id=1, description="Task to save")
        self.task_manager.add_task(task)
        self.task_manager.save_to_file()

        new_manager = TaskManager(filename=self.test_file)
        self.assertIn(1, new_manager.tasks)
        self.assertEqual(new_manager.tasks[1].description,"Task to save")


if __name__ == '__main__':
    unittest.main()
