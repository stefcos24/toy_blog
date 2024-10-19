from rest_framework.permissions import BasePermission


class IsEditor(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.writer.is_editor
        return False
