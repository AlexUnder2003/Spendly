from http import HTTPStatus

from tests.fixture import BaseTestCase


class PublicAccessTests(BaseTestCase):
    """Тесты для маршрутов, доступных всем пользователям."""

    def test_pages_accessible(self):
        urls = (
            self.auth_login_url,
            self.registration_url,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)


class AnonymousAccessTests(BaseTestCase):
    """Тесты для анонимного пользователя."""

    def test_redirect_to_login(self):
        urls = (
            self.dashboard_url,
            self.my_coins_url,
            self.add_coin_url,
            self.edit_coin_url,
            self.update_profile_url,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response, self.auth_login_url + f"?next={url}"
                )


class PrivateAccessTests(BaseTestCase):
    """Тесты маршрутов, доступных только авторизованным пользователям."""

    def test_authorized_pages_accessible(self):
        urls = (
            self.dashboard_url,
            self.my_coins_url,
            self.add_coin_url,
            self.edit_coin_url,
            self.update_profile_url,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_private_pages_unaccessible(self):
        urls = (
            self.my_coins_url,
            self.edit_coin_url,
            self.delete_coin_url,
            self.update_profile_url,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.reader_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
