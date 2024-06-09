from rest_framework.permissions import BasePermission


def is_authenticated(request):
    return request.user.is_authenticated


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_authenticated(request) and (request.user.is_superuser or request.user.role.name == "ADMIN")


class IsDispatcher(BasePermission):
    def has_permission(self, request, view):
        return is_authenticated(request) and request.user.role.name == "DISPATCHER"


class IsAccounting(BasePermission):
    def has_permission(self, request, view):
        return is_authenticated(request) and request.user.role.name == "ACCOUNTING"


class IsHR(BasePermission):
    def has_permission(self, request, view):
        return is_authenticated(request) and request.user.role.name == "HR"


class HasAccessToDashboardPanel(BasePermission):
    def has_permission(self, request, view):
        return any([
            IsSuperAdmin().has_permission(request, view),
            IsDispatcher().has_permission(request, view),
            IsAccounting().has_permission(request, view),
            IsHR().has_permission(request, view)
        ])


class HasAccessToLoadBoardPanel(BasePermission):
    def has_permission(self, request, view):
        return any([
            IsSuperAdmin().has_permission(request, view),
            IsDispatcher().has_permission(request, view)
        ])


class HasAccessToMyBidsPanel(BasePermission):
    def has_permission(self, request, view):
        return any([
            IsSuperAdmin().has_permission(request, view),
            IsDispatcher().has_permission(request, view)
        ])


class HasAccessToMyLoadsPanel(BasePermission):
    def has_permission(self, request, view):
        return any([
            IsSuperAdmin().has_permission(request, view),
            IsDispatcher().has_permission(request, view),
            IsAccounting().has_permission(request, view)
        ])
