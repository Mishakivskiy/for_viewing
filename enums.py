from django.db.models.enums import TextChoices


class UserRoleChoices(TextChoices):
    admin = "admin", "Admin"
    user = "user", "User"


class UserStatusChoices(TextChoices):
    active = "active", "Active"
    inactive = "inactive", "Inactive"

