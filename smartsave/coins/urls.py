from django.urls import path

from .views import my_coins, add_coin


app_name = 'coins'


urlpatterns = [
    path('', my_coins, name='my_coins'),
    path('add_coin/', add_coin, name='add_coin'),
]
