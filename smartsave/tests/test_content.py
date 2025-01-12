from http import HTTPStatus

from coins.forms import AddCoinForm, EditCoinForm
from users.forms import MyUserUpdateForm
from tests.fixture import BaseTestCase


class DashboardViewTests(BaseTestCase):
    """Тесты для дэшборда."""

    def test_user_coins(self):
        for url, user, expected_coins in [
            (self.dashboard_url, self.reader_client, self.expected_coin_data),
            (self.dashboard_url, self.author_client, self.expected_coin_data),
            (self.my_coins_url, self.author_client, self.expected_coin_data),
        ]:
            with self.subTest(user=user):
                response = user.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                if user is self.author_client:
                    self.assertEqual(
                        expected_coins["name"],
                        response.context["coins"][0]["name"],
                    )
                    self.assertEqual(
                        expected_coins["quantity"],
                        response.context["coins"][0]["quantity"],
                    )
                    self.assertEqual(
                        expected_coins["symbol"],
                        response.context["coins"][0]["symbol"],
                    )

                else:
                    self.assertNotIn(expected_coins, response.context["coins"])


class ProfileViewTests(BaseTestCase):
    """Тесты для профиля."""

    def test_author_user_profile(self):
        username = "author_user"
        response = self.author_client.get(
            self.update_profile_url, {"username": username}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], MyUserUpdateForm)

        self.assertEqual(response.context["object"].username, username)
