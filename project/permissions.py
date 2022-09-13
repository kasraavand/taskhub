from rest_framework.permissions import BasePermission


class UserIsManager(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'manager'


class UserIsProjectOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.manager == request.user