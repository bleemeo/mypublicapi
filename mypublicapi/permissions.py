from django.http import Http404
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework import permissions


class DjangoObjectPermissions(permissions.DjangoObjectPermissions):

    def has_permission(self, request, view):
        detail_views = [
            # Standard rest_framework detail views
            'retrieve', 'update', 'partial_update', 'destroy',
        ]
        if hasattr(view, 'action') and view.action in detail_views:
            # All those views call get_object() which call
            # has_object_permission.
            return True

        return super(DjangoObjectPermissions, self).has_permission(
            request, view
        )
