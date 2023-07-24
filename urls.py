from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.user.views import CompanyViewSet, RegisterView, UserViewSet

user_router = DefaultRouter()
user_router.register("company", CompanyViewSet)
user_router.register("", UserViewSet)

app_name = "user"
urlpatterns = [
    path("", include(user_router.urls)),
    path(r"auth/register/", RegisterView.as_view(), name="register"),
]
