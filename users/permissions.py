from rest_framework.permissions import BasePermission
from users.models import User


class IsStandardUser(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(
                email=request.user,
                is_main=False
            )
        except User.DoesNotExist:
            return False
        return True

class IsMainUser(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(
                email=request.user,
                is_main=True
            )
        except User.DoesNotExist:
            return False
        return True