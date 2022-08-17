from rest_framework.permissions import BasePermission
from .services.warehouse_account import get_warehouse_account_by_headers


class IsAuthPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(get_warehouse_account_by_headers(request.headers))


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return get_warehouse_account_by_headers(request.headers).id == obj.warehouse_account.id
