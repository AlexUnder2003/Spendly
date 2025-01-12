from http import HTTPStatus

from coins.models import DailyBalance, UserCoin
from tests.fixture import BaseTestCase
from unittest.mock import patch
from decimal import Decimal
from coins.tasks import calculate_daily_balance


class CoinsAddTests(BaseTestCase):
    """Тесты добавления монет в mycoins."""

    def test_authenticated_user_can_add(self):
        UserCoin.objects.all().delete()

        response = self.author_client.post(self.add_coin_url, self.form_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        user_coin = UserCoin.objects.get()

        self.assertEqual(user_coin.coin_id, self.form_data["coin_id"])
        self.assertEqual(user_coin.quantity, self.form_data["quantity"])

    def test_anonymous_user_cant_add(self):
        UserCoin.objects.all().delete()

        response = self.client.post(self.add_coin_url, self.form_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(UserCoin.objects.count(), 0)


class CoinsEditDeleteTests(BaseTestCase):
    """Тесты редактирования и удаления монет."""

    def test_author_can_delete_coin(self):

        response = self.author_client.post(self.delete_coin_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(UserCoin.objects.all().count(), 0)

    def test_reader_cannot_delete_coin(self):

        response = self.reader_client.post(self.delete_coin_url)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(UserCoin.objects.all().count(), 1)

    def test_author_can_edit_coin(self):
        for user, quantity in ((self.author_client, 2),):
            with self.subTest(user=user):
                response = user.post(self.edit_coin_url, self.edit_form_data)

                updated_coin = UserCoin.objects.get(
                    id=self.coin_by_author.coin_id
                )

                self.assertEqual(response.status_code, HTTPStatus.FOUND)
                self.assertEqual(updated_coin.quantity, quantity)

    def test_reader_cannot_edit_coin(self):
        for user, quantity in ((self.reader_client, 1),):
            with self.subTest(user=user):
                response = user.post(self.edit_coin_url, self.edit_form_data)

                updated_coin = UserCoin.objects.get(
                    id=self.coin_by_author.coin_id
                )

                self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
                self.assertEqual(int(updated_coin.quantity), quantity)


class GetChartDataTests(BaseTestCase):
    """Тесты для api"""

    def test_chart_data_with_date_range(self):
        start_date = "2023-01-01"
        end_date = "2023-01-02"

        response = self.author_client.get(
            self.chart_api_url,
            {"start_date": start_date, "end_date": end_date},
        )

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        chart_labels = response_data["labels"]
        chart_data = response_data["data"]

        self.assertIn("2023-01-01", chart_labels)
        self.assertIn("2023-01-02", chart_labels)
        self.assertNotIn("2023-01-03", chart_labels)

        self.assertEqual(chart_data, ["100.00", "200.00"])

    def test_chart_data_with_no_records(self):
        """Проверяем ситуацию, когда данных нет для заданного диапазона дат."""
        start_date = "2023-02-01"
        end_date = "2023-02-10"

        response = self.author_client.get(
            self.chart_api_url,
            {"start_date": start_date, "end_date": end_date},
        )

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data["labels"], [])
        self.assertEqual(response_data["data"], [])


class CalculateDailyBalanceTests(BaseTestCase):

    @patch("coins.tasks.get_coin_prices")
    def test_calculate_daily_balance_create_new_balance(
        self, mock_get_coin_prices
    ):
        DailyBalance.objects.all().delete()

        mock_get_coin_prices.return_value = {
            "Bitcoin": "10000.00",
        }

        result = calculate_daily_balance()

        daily_balance = DailyBalance.objects.get(
            user=self.author_user, date=self.today
        )
        self.assertEqual(daily_balance.balance, Decimal("10000.00"))

        self.assertEqual(
            result, "Daily balances updated for 1 users with coins"
        )
        self.assertEqual(DailyBalance.objects.all().count(), 1)
