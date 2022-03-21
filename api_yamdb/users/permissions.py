from rest_framework import permissions

from .models import User


class AdminOnly(permissions.BasePermission):
    """Пользователь является администратором."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == User.ADMIN
                 or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == User.ADMIN
            or request.user.is_superuser
        )


class NotAuthenticatedOnly(permissions.BasePermission):
    """Пользователь не аутентифицирован."""

    def has_permission(self, request, view):
        return (
            not request.user.is_authenticated
        )


class AuthorPermission(permissions.BasePermission):
    """Пользователь является автором, админом или модератором."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        c_user_role = request.user.role
        if c_user_role == 'admin' or c_user_role == 'moderator':
            return True
        return obj.author == request.user


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.role == User.ADMIN
                 or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.role == User.ADMIN
                 or request.user.is_superuser)
        )
