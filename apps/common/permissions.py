from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.roles.name == "ADMIN")


class IsDispatcher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.name == "DISPATCHER"


class IsAccounting(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.name == "ACCOUNTING"


class IsHR(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.name == "HR"


class IsAdminOrDispatcher(BasePermission):
    def has_permission(self, request, view):
        return IsAdmin().has_permission(request, view) or IsDispatcher().has_permission(request, view)


class IsAdminOrHR(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.roles.name == "ADMIN" or request.user.roles.name == "HR"
        )
