from django.contrib.auth import get_user_model
from django_filters.rest_framework.filterset import FilterSet

UserModel = get_user_model()


class UserFilterSet(FilterSet):
    class Meta:
        model = UserModel
        fields = ("role", "status")
