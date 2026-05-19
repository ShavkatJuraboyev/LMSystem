from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("roles/", views.role_list, name="role_list"),
    path("roles/create/", views.role_create, name="role_create"),
    path("roles/<uuid:pk>/edit/", views.role_edit, name="role_edit"),
    path("roles/<uuid:pk>/delete/", views.role_delete, name="role_delete"),
    path("roles/<uuid:pk>/permissions/", views.role_permission_update, name="role_permission_update"),

    path("user-roles/", views.user_role_list, name="user_role_list"),
    path("user-roles/create/", views.user_role_create, name="user_role_create"),
    path("user-roles/create-multiple/", views.user_multi_role_create, name="user_multi_role_create"),
    path("user-roles/<uuid:pk>/edit/", views.user_role_edit, name="user_role_edit"),
    path("user-roles/<uuid:pk>/delete/", views.user_role_delete, name="user_role_delete"),
]