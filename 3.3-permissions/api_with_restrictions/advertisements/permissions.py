from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение для объектов, позволяющее только владельцам редактировать их."""
    
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True

        return obj.creator == request.user