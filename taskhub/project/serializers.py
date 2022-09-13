from rest_framework import serializers
from tasks.serializers import TaskUserSerializer
from .models import Project
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    manager = TaskUserSerializer(read_only=True)
    developers = TaskUserSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ("name", "manager", "developers", "date_created")
    
    def to_internal_value(self, data):
        project_name = data.get('name')
        #if it's new, we can safely assume there's no related objects.
        if self.check_is_new_project(project_name):
            return super().to_internal_value(data)
        #it's not new, we handle relations and then let the default do its thing
        self.save_data(project_name, data)
        return super().to_internal_value(data)
    
    def check_is_new_project(self, project_name):
        return not project_name
    
    def save_data(self, project_name, validated_data):
        project = Project.objects.filter(name=project_name).first()

        try:
            developers = validated_data.pop('developers')
        except KeyError:
            developers = []
        else:
            for dev_data in developers:
                dev_qs = User.objects.filter(username__iexact=dev_data['username'])

                if dev_qs.exists():
                    dev = dev_qs.first()
                else:
                    dev = User.objects.create(**dev_data)

                project.developers.add(dev)
        finally:
            return project