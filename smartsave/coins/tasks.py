from __future__ import absolute_import
from decimal import Decimal

from django.utils.timezone import now
from celery import shared_task

from coins.models import UserCoin, DailyBalance, User
from coins.functions import get_coin_prices


@shared_task
def calculate_daily_balance():
    user_ids = UserCoin.objects.values_list("user_id", flat=True).distinct()
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

        # Найти или создать запись о балансе
        daily_balance, created = DailyBalance.objects.get_or_create(
            user=user, date=today, defaults={"balance": total_balance_today}
        )

        # Если запись уже существует, обновляем баланс
        if not created:
            daily_balance.balance = total_balance_today
            daily_balance.save()

    return f"Daily balances updated for {len(users)} users with coins"
