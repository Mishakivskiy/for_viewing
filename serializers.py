from dj_rest_auth.serializers import UserDetailsSerializer as BaseUserDetailsSerializer
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from app.user.models import Company

UserModel = get_user_model()


class UserDetailsSerializer(BaseUserDetailsSerializer):
    phone = PhoneNumberField(required=False)
    available_tables = SerializerMethodField()

    def get_available_tables(self, instance):
        company_id = instance.company_id
        if not company_id:
            return []

        company = Company.objects.only("available_tables").get(pk=company_id)
        return company.available_tables

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "available_tables",
        )
        read_only_fields = ("id",)


class UserRegisterSerializer(ModelSerializer):
    phone = PhoneNumberField(required=False)

    def create(self, validated_data: dict):
        password = validated_data.pop("password")
        username = validated_data.pop("username")

        user = UserModel(
            username=UserModel.normalize_username(username), **validated_data
        )
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = (
            "username",
            "email",
            "phone",
            "company",
            "first_name",
            "last_name",
            "password",
        )
        write_only_fields = ("password",)
        extra_kwargs = {
            "password": {"write_only": True},
            "company": {"required": True},
        }


class CompanySerializer(ModelSerializer):
    phone = PhoneNumberField(required=False)

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "description",
            "email",
            "phone",
            "available_tables",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
