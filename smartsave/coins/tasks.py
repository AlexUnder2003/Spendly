from __future__ import absolute_import
from decimal import Decimal
from celery import shared_task
from .models import UserCoin, DailyBalance, User
from .functions import get_coin_prices
from django.utils.timezone import now


@shared_task
def calculate_daily_balance():
    user_ids = UserCoin.objects.values_list('user_id', flat=True).distinct()
    users = User.objects.filter(id__in=user_ids)
    prices = get_coin_prices()
    today = now().date()

    for user in users:
        coins = UserCoin.objects.filter(user=user)
        total_balance_today = 0

        for coin in coins:
            price = Decimal(prices.get(coin.coin.name, 0))
            quantity = coin.quantity
            total_balance_today += price * quantity

        existing_balance = DailyBalance.objects.filter(
            user=user,
            date=today
        ).first()

        if not existing_balance:
            DailyBalance.objects.create(
                user=user,
                date=today,
                balance=total_balance_today
            )

    return f"Daily balances updated for {len(users)} users with coins"
