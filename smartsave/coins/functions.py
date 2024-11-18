import requests
from decimal import Decimal, ROUND_HALF_UP

from django.core.cache import cache

from coins.models import Coin, UserCoin


def get_coin_prices():
    """
    Получает текущие курсы для каждой монеты с кэшированием.
    Если данные для монеты уже есть в кэше, возвращает их, иначе — запрашивает из API.
    """
    coin_prices = cache.get('coin_prices')

    if not coin_prices or any(price == 0 for price in coin_prices.values()):
        coin_prices = {}
        coins = Coin.objects.all()

        symbols = ",".join(coin.symbol.upper() for coin in coins)
        url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={symbols}&tsyms=USD"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for coin in coins:
                price = data.get(coin.symbol, {}).get('USD')
                coin_prices[coin.name] = price if price is not None else 0

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе данных: {e}")
            coin_prices = {coin.name: None for coin in coins}

        if any(coin_prices.values()):
            cache.set('coin_prices', coin_prices, timeout=600)
        else:
            print("Данные от API не получены; повторный запрос будет выполнен позже.")

    return coin_prices


def get_user_coins(user_id):
    coins = UserCoin.objects.filter(user=user_id)
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

    return coins_with_prices
