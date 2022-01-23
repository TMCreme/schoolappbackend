from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from organizations.backends import invitation_backend
from . import views

app_name = "home"

urlpatterns = [
    path("api-register-user/", views.create_user, name="api-register-user"),
    path('api-login-user/', views.LoginUserView.as_view(), name='api-login-user'),
    path("api-change-password/", views.ChangePasswordView.as_view(), name="api-change-password"),
    path('api-password-reset/', include('django_rest_passwordreset.urls', namespace='api-password-reset')),
    path('api-logout-user/', views.LogoutAPIView.as_view(), name='api-logout-user'),
    path("accounts/", include('organizations.urls')),
    path("invitations/", include(invitation_backend().get_urls())),
    path("api-textbook/", views.TextBookView.as_view(), name="api-textbook"),
] 


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]


