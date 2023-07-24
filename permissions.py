from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from app.user.enums import UserRoleChoices
from app.user.models import Company, User


class IsSelfUser(BasePermission):
    def has_object_permission(self, request: Request, view, obj: User) -> bool:
        return request.user.pk == obj.pk


class IsUserManager(BasePermission):
    def has_object_permission(self, request: Request, view, obj: User) -> bool:
        return (
            request.user.role == UserRoleChoices.manager
            and request.user.company_id == obj.company_id
        )


class IsCompanyManager(BasePermission):
    def has_object_permission(self, request: Request, view, obj: Company) -> bool:
        return (
            request.user.role == UserRoleChoices.manager
            and request.user.company_id == obj.pk
        )
