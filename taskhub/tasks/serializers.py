from rest_framework import serializers
from tasks.models import Task

from django.contrib.auth import get_user_model

User = get_user_model()


class TaskUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "date_joined")


class taskserializer(serializers.ModelSerializer):
    user = TaskUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("project", "user", "name", "done", "date_created")
