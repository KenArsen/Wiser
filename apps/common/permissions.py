from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
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


class HasAccessToDashboardPanel(BasePermission):
    def has_permission(self, request, view):
        return (
            IsSuperAdmin().has_permission(request, view)
            or IsDispatcher().has_permission(request, view)
            or IsAccounting().has_permission(request, view)
            or IsHR().has_permission(request, view)
        )


class HasAccessToLoadBoardPanel(BasePermission):
    def has_permission(self, request, view):
        return IsSuperAdmin().has_permission(request, view) or IsDispatcher().has_permission(request, view)


class HasAccessToMyBidsPanel(BasePermission):
    def has_permission(self, request, view):
        return IsSuperAdmin().has_permission(request, view) or IsDispatcher().has_permission(request, view)


class HasAccessToMyLoadsPanel(BasePermission):
    def has_permission(self, request, view):
        return (
            IsSuperAdmin().has_permission(request, view)
            or IsDispatcher().has_permission(request, view)
            or IsAccounting().has_permission(request, view)
        )
