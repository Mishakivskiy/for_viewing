from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.forms.widgets import CheckboxSelectMultiple

from app.user.fields import ChoiceArrayField
from app.user.models import User


@register(User)
class UserAdmin(AuthUserAdmin):
    search_fields = (
        "^first_name",
        "@first_name",
        "^last_name",
        "@last_name",
        "^email",
        "@email",
        "^phone",
        "@phone",
    )
    list_filter = (
        "role",
        "status",
    )
    readonly_fields = ("id", "last_login", "date_joined")

    def get_fieldsets(self, request, instance=None):
        fieldsets = super().get_fieldsets(request, instance)
        if instance:
            # Personal Info
            fieldsets[1][1]["fields"] = (
                "first_name",
                "last_name",
                "email",
                "company",
                "status",
            )
            # Permissions
            fieldsets[2][1]["fields"] = (
                "is_active",
                "role",
                "groups",
                "user_permissions",
            )
        return fieldsets
