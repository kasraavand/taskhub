from rest_framework.permissions import BasePermission


class UserIsOwnerTask(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'manager':
            return obj.project.owner.id == request.user.id
        return request.user.id == obj.user.id
