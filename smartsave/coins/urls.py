from django.urls import path

from coins.views import my_coins, add_coin, delete_coin, edit_coin


app_name = "coins"


urlpatterns = [
    path("", my_coins, name="my_coins"),
    path("add_coin/", add_coin, name="add_coin"),
    path('delete_coin/<int:coin_id>/', delete_coin, name='delete_coin'),
    path('edit_coin/<int:coin_id>/', edit_coin, name='edit_coin'),
]
