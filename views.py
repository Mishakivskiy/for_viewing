from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from app.common.permissions import IsReadOnly
from app.user.enums import UserRoleChoices
from app.user.filters import UserFilterSet
from app.user.models import Company
from app.user.permissions import IsCompanyManager, IsSelfUser, IsUserManager
from app.user.serializers import (
    CompanySerializer,
    UserDetailsSerializer,
    UserRegisterSerializer,
)

User = get_user_model()


class UserViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated & (IsAdminUser | IsSelfUser | IsUserManager),)
    queryset = User.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filterset_class = UserFilterSet
    search_fields = (
        "^username",
        "@username",
        "^first_name",
        "@first_name",
        "^last_name",
        "@last_name",
        "^email",
        "@email",
        "^phone",
        "@phone",
    )
    ordering_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "company",
        "status",
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == UserRoleChoices.admin:
            return queryset
        if self.request.user.role == UserRoleChoices.manager:
            return queryset.filter(company_id=self.request.user.company_id)

        return queryset.filter(pk=self.request.user.pk)


class CompanyViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = CompanySerializer
    permission_classes = (
        IsReadOnly | (IsAuthenticated & (IsAdminUser | IsCompanyManager)),
    )
    queryset = Company.objects.all()


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
