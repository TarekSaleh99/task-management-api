from rest_framework import serializers
from .models import Task
from projects.models import Project


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'project', 'title',
            'description', 'status', 'assigned_to',
            'due_date', 'created_at', 'updated_at'
            ]
        read_only_fields = ['id', 'created_at', 'updated_at']


    def validate_assigned_to(self, value):
            # Value is list of users assignde to task
        """
        Ensure all assigned users are members of the project
        """
        if not value:
            return value  # Allow empty assignment
        
        if self.instance: # if task already exists <self.instance not None>.
            project = self.instance.project # we get the project from the existing task
        else: # if it's a new task <self.instance is None>
            # Now we get the project from the request data.
            project = self.initial_data.get('project') 

        if not project:
            raise serializers.ValidationError('Project is required.')
        
        non_members = []  # Create an empty list to store invalid users

        for user in value:
            if user not in project.members.all(): # Check if the user is NOT in project members
                non_members.append(user)
        
        if non_members: # if there ary any invalid users
            raise serializers.ValidationError('Some assigned users are not members of the project.')
        
        return value # id all users are valid, return value