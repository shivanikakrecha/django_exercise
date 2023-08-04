from django.urls import path
from .views import ImageUploadView, ImageDetailView, ImageDeleteView
from django.contrib.auth import views as auth_views

app_name = "image_uploader"

urlpatterns = [
    path("", ImageUploadView.as_view(), name="image_upload"),
    path(
        "image/<slug:unique_identifier>/",
        ImageDetailView.as_view(),
        name="image-detail",
    ),
    path(
        "image/<slug:unique_identifier>/delete/",
        ImageDeleteView.as_view(),
        name="image_delete",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="admin/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="admin/logout.html"),
        name="logout",
    ),
]
