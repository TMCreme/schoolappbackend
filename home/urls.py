from django.contrib import admin
from django.urls import path, include
from organizations.backends import invitation_backend
from . import views

app_name = "home"

urlpatterns = [
    path("api-register-user/", views.create_user, name="api-register-user"),
    path('api-login-user/', views.LoginUserView.as_view(), name='api-login-user'),
    path("api-change-password/", views.ChangePasswordView.as_view(), name="api-change-password"),
    path('api-password-reset/', include('django_rest_passwordreset.urls', namespace='api-password-reset')),
    path("accounts/", include('organizations.urls')),
    path("invitations/", include(invitation_backend().get_urls())),
]
