from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
import requests
import os

from .models import Task, Goal
from .serializers import (
    TaskSerializer, TaskDetailSerializer, TaskCreateSerializer,
    GoalSerializer, GoalDetailSerializer, GoalCreateSerializer
)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Purpose: Handles all API requests for tasks 
    (list, create, retrieve, update, delete, mark complete/incomplete)
    """
    queryset = Task.objects.all()
    
    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action."""
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['retrieve', 'mark_complete', 'mark_incomplete']:
            return TaskDetailSerializer
        return TaskSerializer

    def create(self, request, *args, **kwargs):
        """Create a new task, optionally assigning it to a goal."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Handle goal_id from request data
        goal_id = request.data.get('goal_id')
        if goal_id:
            try:
                goal = Goal.objects.get(id=goal_id)
                task = serializer.save(goal=goal)
            except Goal.DoesNotExist:
                return Response(
                    {"error": "Goal not found"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            task = serializer.save()
        
        # Return the created task with full details
        detail_serializer = TaskDetailSerializer(task)
        return Response(
            {"task": detail_serializer.data}, 
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        """List all tasks."""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single task by ID."""
        task = self.get_object()
        serializer = TaskDetailSerializer(task)
        return Response({"task": serializer.data})

    def update(self, request, *args, **kwargs):
        """Update a task by ID."""
        task = self.get_object()
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        """Delete a task by ID."""
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def mark_complete(self, request, pk=None):
        """Mark a task as complete and send a Slack notification."""
        task = self.get_object()
        
        if task.is_complete:
            return Response(
                {"error": "Task is already complete"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.mark_complete()
        
        # Send Slack notification
        self._send_slack_notification(task, "completed")
        
        serializer = TaskDetailSerializer(task)
        return Response({"task": serializer.data})

    @action(detail=True, methods=['patch'])
    def mark_incomplete(self, request, pk=None):
        """Mark a task as incomplete."""
        task = self.get_object()
        
        if not task.is_complete:
            return Response(
                {"error": "Task is already incomplete"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.mark_incomplete()
        
        serializer = TaskDetailSerializer(task)
        return Response({"task": serializer.data})

    def _send_slack_notification(self, task, action):
        """Send notification to Slack when task is completed."""
        slack_token = os.getenv('SLACK_API_TOKEN')
        slack_channel = os.getenv('SLACK_CHANNEL', 'task-notifications')
        
        if not slack_token:
            return
        
        slack_url = "https://slack.com/api/chat.postMessage"
        slack_headers = {"Authorization": f"Bearer {slack_token}"}
        slack_data = {
            "channel": slack_channel,
            "text": f"Someone just {action} the task: {task.title}"
        }
        
        try:
            response = requests.post(slack_url, headers=slack_headers, json=slack_data)
            if response.status_code == 200:
                response_data = response.json()
                if not response_data.get('ok'):
                    print(f"Slack API error: {response_data.get('error')}")
        except Exception as e:
            print(f"Slack notification failed: {e}")


class GoalViewSet(viewsets.ModelViewSet):
    """
    Purpose: Handles all API requests for goals (list, create, retrieve, update, delete)
    """
    queryset = Goal.objects.all()
    
    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action."""
        if self.action == 'create':
            return GoalCreateSerializer
        elif self.action in ['retrieve', 'tasks']:
            return GoalDetailSerializer
        return GoalSerializer

    def create(self, request, *args, **kwargs):
        """Create a new goal."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        goal = serializer.save()
        
        detail_serializer = GoalDetailSerializer(goal)
        return Response(
            {"goal": detail_serializer.data}, 
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        """List all goals."""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single goal by ID."""
        goal = self.get_object()
        serializer = GoalDetailSerializer(goal)
        return Response({"goal": serializer.data})

    def update(self, request, *args, **kwargs):
        """Update a goal by ID."""
        goal = self.get_object()
        serializer = GoalSerializer(goal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        """Delete a goal by ID."""
        goal = self.get_object()
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)