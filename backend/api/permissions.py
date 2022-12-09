"""Создание разрешений."""

from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Админ имеет разрешение на чтение и запись."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_superuser
        )


class AdminOrAuthor(permissions.BasePermission):
    """Админ и автор имеют разрешения на чтение и запись."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.is_superuser
        )
