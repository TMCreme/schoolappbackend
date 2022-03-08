from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from organizations.backends import invitation_backend
from . import views

app_name = "home"

urlpatterns = [
    path("api-register-user/", views.create_user, name="api-register-user"),
    path('api-login-user/', views.LoginUserView.as_view(), name='api-login-user'),
    path("api-change-password/", views.ChangePasswordView.as_view(), name="api-change-password"),
    path('api-password-reset/', include('django_rest_passwordreset.urls', namespace='api-password-reset')),
    path('api-logout-user/', views.LogoutAPIView.as_view(), name='api-logout-user'),
    path("api-admin-password-reset/", views.AdminPasswordResetView.as_view(), name="api-admin-password-reset"),
    path("accounts/", include('organizations.urls')),
    path("invitations/", include(invitation_backend().get_urls())),
    path("api-textbook/", views.TextBookView.as_view(), name="api-textbook"),
    path("api-admin-student-list/", views.SchoolAdminStudentView.as_view(), name="api-admin-student-list"),
    path("api-student-parent-link/", views.StudentParentRelationView.as_view(), name="api-student-parent-link"),
    path("api-student-link-level/", views.StudentLinkLevel.as_view(), name="api-student-link-level"),
    path("api-student-level-update/", views.StudentLevelUpdate.as_view(), name="api-student-level-update"),
    path("api-admin-user-list/", views.AdminUserList.as_view(), name="api-admin-user-list"),
    path("api-teacher-subject-list/", views.TeacherSubjectView.as_view(), name="api-teacher-subject-list"),
    path("api-parent-student-view/", views.ParentStudentView.as_view(), name="api-parent-student-view"),
    path("api-add-ptaschedule/", views.PTAScheduleView.as_view(), name="api-add-ptaschedule"),
    path("api-admin-add-student-remark/", views.AdminRemarkForStudentView.as_view(),name='api-admin-add-student-remark'),
    path("api-student-list-for-subject/", views.StudentListForSubjectView.as_view(), name="api-student-view-for-subject"),
    path("api-teacher-add-assignment/", views.PostAssignmentView.as_view(), name="api-teacher-add-assignment"),
    path("api-admin-list-classes/", views.LevelListView.as_view(), name="api-admin-list-classes"),
    path("api-admin-upload-class-timetable/", views.ClassTimeTableView.as_view(), name="api-admin-upload-class-timetable"),
    path("api-admin-download-time-table/", views.ClassTimeTableDownloadview.as_view(), name="api-admin-download-time-table"),
    
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


