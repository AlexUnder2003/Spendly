from django.urls import path
from .views import AddCoinView, MyCoinsView, DeleteCoinView, EditCoinView

app_name = "coins"


urlpatterns = [
    path("add/", AddCoinView.as_view(), name="add_coin"),
    path("mycoins/<slug:username>", MyCoinsView.as_view(), name="my_coins"),
    path(
        "delete/<str:username>/<int:coin_id>/",
        DeleteCoinView.as_view(),
        name="delete_coin",
    ),
    path(
        "edit/<str:username>/<int:coin_id>/",
        EditCoinView.as_view(),
        name="edit_coin",
    ),
]
