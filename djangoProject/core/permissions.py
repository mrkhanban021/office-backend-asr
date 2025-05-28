from rest_framework.permissions import SAFE_METHODS, BasePermission


class CustomerAccessPermission(BasePermission):
    message = 'Only superusers can modify customer data.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS :
            return True
        return request.user and request.user.is_superuser
