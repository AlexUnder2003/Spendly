from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from coins.models import Coin, DailyBalance, UserCoin

User = get_user_model()


class BaseTestCase(TestCase):
    """Базовый класс для тестов."""

    @classmethod
    def setUpTestData(cls):
        cls.reader_user = User.objects.create_user(username="reader_user")
        cls.author_user = User.objects.create_user(username="author_user")

        cls.coin_btc = Coin.objects.create(
            name="Bitcoin",
            symbol="BTC",
        )

        cls.coin_by_author = UserCoin.objects.create(
            user=cls.author_user,
            coin=cls.coin_btc,
            coin_id=1,
            quantity=1,
        )

        DailyBalance.objects.bulk_create(
            [
                DailyBalance(
                    user=cls.author_user,
                    date=date(2023, 1, 1),
                    balance=Decimal("100.00"),
                ),
                DailyBalance(
                    user=cls.author_user,
                    date=date(2023, 1, 2),
                    balance=Decimal("200.00"),
                ),
                DailyBalance(
                    user=cls.author_user,
                    date=date(2023, 1, 3),
                    balance=Decimal("300.00"),
                ),
            ]
        )

        cls.form_data = {
            "coin_id": 1,
            "quantity": 1,
        }

        cls.edit_form_data = {
            "quantity": 2,
        }

        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader_user)

        cls.author_client = Client()
        cls.author_client.force_login(cls.author_user)

        cls.auth_login_url = reverse("login")
        cls.auth_logout_url = reverse("logout")
        cls.registration_url = reverse("registration")
        cls.dashboard_url = reverse("dashboard:dashboard")
        cls.chart_data_url = reverse("dashboard:chart_data")
        cls.my_coins_url = reverse(
            "coins:my_coins", args=[cls.author_user.username]
        )
        cls.add_coin_url = reverse("coins:add_coin")
        cls.expected_coin_data = {
            "name": cls.coin_by_author.coin.name,
            "symbol": cls.coin_by_author.coin.symbol,
            "quantity": cls.coin_by_author.quantity,
        }
        cls.delete_coin_url = reverse(
            "coins:delete_coin",
            kwargs={"username": cls.author_user.username, "coin_id": 1},
        )
        cls.edit_coin_url = reverse(
            "coins:edit_coin",
            kwargs={"username": cls.author_user.username, "coin_id": 1},
        )
        cls.update_profile_url = reverse(
            "update_profile", args=[cls.author_user.username]
        )
        cls.chart_api_url = reverse("dashboard:chart_data")
        cls.today = now().date()
