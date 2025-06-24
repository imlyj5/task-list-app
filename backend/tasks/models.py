from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    """Base model with created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Goal(BaseModel):
    """Goal category model"""
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def to_dict(self):
        """Return a dictionary representation of the goal, including its tasks."""
        goal_as_dict = {}
        goal_as_dict["id"] = self.id
        goal_as_dict["title"] = self.title
        if self.tasks.exists():
            goal_as_dict["tasks"] = [task.to_dict() for task in self.tasks.all()]
        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):
        """Create a Goal instance from a dictionary."""
        new_goal = cls(title=goal_data["title"])
        return new_goal

    class Meta:
        ordering = ['-created_at']

class Task(BaseModel):
    """Model representing a task, which can belong to a goal."""
    title = models.CharField(max_length=200)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')

    def __str__(self):
        return self.title

    def to_dict(self):
        """Return a dictionary representation of the task."""
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        if self.completed_at:
            task_as_dict["completed_at"] = self.completed_at
        if self.is_complete:
            task_as_dict["is_complete"] = self.is_complete
        else:
            task_as_dict["is_complete"] = False
        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id
        return task_as_dict

    @classmethod
    def from_dict(cls, task_data):
        """Create a Task instance from a dictionary."""
        goal_id = task_data.get("goal_id")
        new_task = cls(
            title=task_data["title"],
            completed_at=task_data.get("completed_at", None),
            is_complete=task_data.get("is_complete", False),
            goal_id=goal_id
        )
        return new_task

    def mark_complete(self):
        """Mark the task as complete and set the completion timestamp."""
        self.is_complete = True
        self.completed_at = timezone.now()
        self.save()

    def mark_incomplete(self):
        """Mark the task as incomplete and clear the completion timestamp."""
        self.is_complete = False
        self.completed_at = None
        self.save()

    class Meta:
        ordering = ['-created_at'] 