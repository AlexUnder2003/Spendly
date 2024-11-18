from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from .forms import AddCoinForm
from .models import UserCoin
from .functions import get_coin_prices
from .tasks import calculate_daily_balance


def task(request):
    user_id = request.user.id

    result = calculate_daily_balance.apply_async((user_id,))

    try:
        result_value = result.get(timeout=10)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', content_type='text/plain')

    return HttpResponse(f'Result: {result_value}', content_type='text/plain')


@login_required
def add_coin(request):
    if request.method == 'POST':
        form = AddCoinForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('dashboard:dashboard')
    else:
        form = AddCoinForm()

    return render(request, 'coins/add_coin.html', {'form': form})


@login_required
def my_coins(request):
    coins = UserCoin.objects.filter(user=request.user)
    prices = get_coin_prices()

    coins_with_prices = [
        {
            "name": coin.coin.name,
            "symbol": coin.coin.symbol,
            "quantity": coin.quantity,
            "price": prices.get(coin.coin.name, 0),
            "value": (coin.quantity * Decimal(prices.get(coin.coin.name, 0))).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        }
        for coin in coins
    ]

    context = {'coins': coins_with_prices}

    return render(request, 'coins/my_coins.html', context)
