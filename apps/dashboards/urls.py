from django.urls import path
from .views import DashboardsView, get_chart_data
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "",
        login_required(DashboardsView.as_view(template_name="dashboard_crm.html")),
        name="index",
    ),

    path(
        "dashboard/crm/",
        login_required(DashboardsView.as_view(template_name="dashboard_crm.html")),
        name="dashboard-crm",
    ),
    path(
        "get_chat_data/",
        login_required(get_chart_data),
        name="get-json-data",
    ),
]
