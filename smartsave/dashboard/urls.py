from django.urls import path
from .views import dashboard_view, get_chart_data

app_name = 'dashboard'

urlpatterns = [
    path('api/chart-data/', get_chart_data, name='chart_data'),
    path('', dashboard_view, name='dashboard'),
]
