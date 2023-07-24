from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CIEmailField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.db.models import CharField, DateTimeField, ForeignKey, Model, TextField
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from app.user.enums import UserRoleChoices, UserStatusChoices
from app.user.fields import ChoiceArrayField


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = CIEmailField(max_length=50, unique=True)
    phone = PhoneNumberField(_("Phone number"), blank=True)

    role = CharField(
        max_length=10, choices=UserRoleChoices.choices, default=UserRoleChoices.user
    )
    status = CharField(
        max_length=10,
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.inactive,
    )

    user_reports = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField()

    class Meta:
        indexes = (
            GinIndex(
                SearchVector(
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    config="english",
                ),
                name="user_search_vector",
            ),
        )
