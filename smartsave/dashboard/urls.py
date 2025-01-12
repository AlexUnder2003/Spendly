from django.urls import path
from .views import DashboardView, get_chart_data

app_name = "dashboard"

urlpatterns = [
    path("api/chart-data/", get_chart_data, name="chart_data"),
    path("", DashboardView.as_view(), name="dashboard"),
]
