from django.contrib import admin
from django.urls import path, include

from task_manager.views import profile_redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("task_manager.urls", namespace="task_manager")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", profile_redirect, name="profile"),
]
