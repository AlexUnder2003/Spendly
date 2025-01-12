from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView

from users.views import UpdateProfile
from users.forms import CustomUserCreationForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "auth/registration/",
        CreateView.as_view(
            template_name="registration/registration_form.html",
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy("dashboard:dashboard"),
        ),
        name="registration",
    ),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("coins/", include("coins.urls", namespace="coins")),
    path(
        "profile/update/<str:username>",
        UpdateProfile.as_view(),
        name="update_profile",
    ),
    path(
        "",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
]
