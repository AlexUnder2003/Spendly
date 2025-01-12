from decimal import Decimal, ROUND_HALF_UP


from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    ListView,
    DeleteView,
    UpdateView,
)
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404, HttpResponse

from coins.forms import AddCoinForm, EditCoinForm
from coins.models import UserCoin
from coins.functions import get_coin_prices
from coins.tasks import calculate_daily_balance


User = get_user_model()


def task(request):
    user_id = request.user.id

    result = calculate_daily_balance.apply_async((user_id,))

    try:
        result_value = result.get(timeout=10)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", content_type="text/plain")

    return HttpResponse(f"Result: {result_value}", content_type="text/plain")


class AuthUserTest(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user


class AddCoinView(LoginRequiredMixin, FormView):
    template_name = "coins/add_coin.html"
    form_class = AddCoinForm

    def form_valid(self, form):
        form.save(user=self.request.user)
        return redirect("dashboard:dashboard")

    def form_invalid(self, form):
        return self.render_to_response({"form": form})


class MyCoinsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserCoin
    template_name = "coins/my_coins.html"
    context_object_name = "coins"

    def get_queryset(self):
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username=username)

        coins = UserCoin.objects.filter(user=user)
        prices = get_coin_prices()

        coins_with_prices = [
            {
                "name": coin.coin.name,
                "symbol": coin.coin.symbol,
                "quantity": coin.quantity,
                "price": prices.get(coin.coin.name, 0),
                "value": (
                    Decimal(coin.quantity)
                    * Decimal(prices.get(coin.coin.name, 0))
                ).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP),
                "id": coin.coin.id,
            }
            for coin in coins
        ]
        return coins_with_prices

    def test_func(self):
        username = self.kwargs.get("username")
        return username == self.request.user.username


class DeleteCoinView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserCoin
    success_url = reverse_lazy("coins:my_coins")
    template_name = "coins/confirm_delete.html"

    def get_object(self, queryset=None):
        coin_id = self.kwargs.get("coin_id")
        username = self.kwargs.get("username")
        obj = get_object_or_404(
            UserCoin, coin_id=coin_id, user__username=username
        )

        return obj

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["coin_name"] = self.get_object().coin.name
        return context

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy("coins:my_coins", kwargs={"username": username})


class EditCoinView(LoginRequiredMixin, AuthUserTest, UpdateView):
    model = UserCoin
    form_class = EditCoinForm
    template_name = "coins/edit_coin.html"

    def get_object(self, queryset=None):
        coin_id = self.kwargs.get("coin_id")
        username = self.kwargs.get("username")
        obj = get_object_or_404(
            UserCoin, coin_id=coin_id, user__username=username
        )
        return obj

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy("coins:my_coins", kwargs={"username": username})
