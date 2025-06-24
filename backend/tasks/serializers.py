from rest_framework import serializers
from .models import Task, Goal

# Convert model instances to JSON for API responses
# Validate and process incoming data for creating or updating models via the API

class TaskSerializer(serializers.ModelSerializer):
    """List/detail view for Task model"""
    # Include goal_id and goal_title fields for nested goal information
    goal_id = serializers.IntegerField(source='goal.id', read_only=True)
    goal_title = serializers.CharField(source='goal.title', read_only=True)

    class Meta:  #Specifies which fields to include in the output
        model = Task
        fields = [
            'id', 'title', 'completed_at', 
            'is_complete', 'goal_id', 'goal_title', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

    def create(self, validated_data):
        """Custom create method to handle goal assignment if provided in context."""
        goal_id = self.context.get('goal_id')
        if goal_id:
            try:
                goal = Goal.objects.get(id=goal_id)
                validated_data['goal'] = goal
            except Goal.DoesNotExist:
                raise serializers.ValidationError("Goal not found")
        
        return super().create(validated_data)


class TaskDetailSerializer(TaskSerializer):
    """Detailed task view (with goal)"""
    
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['goal']


class GoalSerializer(serializers.ModelSerializer):
    """List/detail of goals"""
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = ['id', 'title', 'tasks', 'task_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_task_count(self, obj):
        """Return the number of tasks associated with this goal."""
        return obj.tasks.count()


class GoalDetailSerializer(GoalSerializer):
    """Detailed goal view"""
    
    class Meta(GoalSerializer.Meta):
        fields = GoalSerializer.Meta.fields


class TaskCreateSerializer(serializers.ModelSerializer):
    """Creating a task"""
    
    class Meta:
        model = Task
        fields = ['title', 'goal_id']
        extra_kwargs = {
            'goal_id': {'required': False}
        }

    def validate_goal_id(self, value):
        """Ensure the provided goal_id exists if given."""
        if value is not None:
            try:
                Goal.objects.get(id=value)
            except Goal.DoesNotExist:
                raise serializers.ValidationError("Goal not found")
        return value


class GoalCreateSerializer(serializers.ModelSerializer):
    """Creating a goal"""
    
    class Meta:
        model = Goal
        fields = ['title'] 