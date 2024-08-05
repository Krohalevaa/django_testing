from http import HTTPStatus

from notes.tests.common import URL, BaseTestCase, AUTHOR, JUST_USER, ANON


class TestRoutes(BaseTestCase):
    def test_pages_availability(self):
        """Доступность страниц"""
        urls = (
            (URL.home, self.client, HTTPStatus.OK, ANON),
            (URL.login, self.client, HTTPStatus.OK, ANON),
            (URL.logout, self.client, HTTPStatus.OK, ANON),
            (URL.signup, self.client, HTTPStatus.OK, ANON),
            (URL.detail, self.author_client, HTTPStatus.OK, AUTHOR),
            (URL.edit, self.author_client, HTTPStatus.OK, AUTHOR),
            (URL.delete, self.author_client, HTTPStatus.OK, AUTHOR),
            (URL.add, self.user_client, HTTPStatus.OK, JUST_USER),
            (URL.list, self.user_client, HTTPStatus.OK, JUST_USER),
            (URL.success, self.user_client, HTTPStatus.OK, JUST_USER),
            (URL.detail, self.user_client, HTTPStatus.NOT_FOUND, JUST_USER),
            (URL.edit, self.user_client, HTTPStatus.NOT_FOUND, JUST_USER),
            (URL.delete, self.user_client, HTTPStatus.NOT_FOUND, JUST_USER),
        )
        for url, client, expected_status, user in urls:
            with self.subTest("Страница не доступна", url=url):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        """Редирект со страниц если пользователь анонимный."""
        urls = (
            URL.list,
            URL.add,
            URL.success,
            URL.detail,
            URL.edit,
            URL.delete,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{URL.login}?next={url}'
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url)
