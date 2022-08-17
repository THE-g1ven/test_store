from rest_framework.permissions import BasePermission
from .services.store_account import get_store_account_by_headers


class IsAuthPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(get_store_account_by_headers(request.headers))


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return get_store_account_by_headers(request.headers).id == obj.store_account.id
