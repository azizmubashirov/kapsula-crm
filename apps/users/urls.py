from django.urls import path
from .views import UsersView, CLientUpdateDetailView, delete_user, export_clients_to_excel, import_clients_from_excel
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/user/list/",
        login_required(UsersView.as_view(template_name="app_user_list.html")),
        name="app-user-list",
    ),
    path(
        "app/user/create/",
        login_required(UsersView.as_view(template_name="app_user_create.html")),
        name="app-user-create",
    ),
    path(
        "app/user/<int:pk>/edit/",
        login_required(CLientUpdateDetailView.as_view(template_name="app_user_create.html")),
        name="app-user-edit",
    ),
    path(
        "app/user/<int:pk>/delete/",
        login_required(delete_user),
        name="app-user-delete",
    ),
    path(
        "app/user/<int:pk>/view/account/",
        login_required(CLientUpdateDetailView.as_view(template_name="app_user_view_account.html")),
        name="app-user-view-account",
    ),
    path(
        "app/user/export/data", export_clients_to_excel
    ),
    path(
        "app/import/clients", import_clients_from_excel
    )
]
