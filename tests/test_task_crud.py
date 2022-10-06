from tests.common import ReclaimTestCase


class TestTaskCRUD(ReclaimTestCase):
    def test_task_creation(self):
        """
        Tests the creation of a task at reclaim.ai
        """
        self.assertTrue(self.test_task.id is not None)

        with self.test_task as task:
            # We set the date fields and the duration
            task.duration = 10
            task.start_date = "2050-01-01T07:00:00.000Z"
            task.due_date = "2050-01-31T17:00:00.000Z"
            task.min_work_duration = 0.78
            task.max_work_duration = 1.62
            task.description = "This is a test task"

        # We check if the task was saved correctly
        self.assertEqual(self.test_task.duration, 10)
        self.assertEqual(self.test_task.min_work_duration, 0.75)
        self.assertEqual(self.test_task.max_work_duration, 1.5)

        # Now we mark the task as complete
        self.test_task.mark_complete()
        self.assertEqual(self.test_task["status"], "ARCHIVED")

        # And we mark the task as incomplete again
        self.test_task.mark_incomplete()
        self.assertNotEqual(self.test_task["status"], "ARCHIVED")

        # We delete the task again and check if it was deleted
        task_id = self.test_task.id
        self.test_task.delete()

        with self.assertRaises(ValueError):
            self.test_task.get(task_id)
