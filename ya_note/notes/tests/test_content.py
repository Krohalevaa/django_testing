from notes.forms import NoteForm
from notes.tests.common import URL, BaseTestCase


class TestContentPage(BaseTestCase):
    def test_note_in_list_for_different(self):
        """Отдельная заметка передаётся на страницу со списком заметок"""
        clients = (
            (self.author_client, True),
            (self.user_client, False),
        )
        for client, value in clients:
            with self.subTest(client=client):
                object_list = client.get(URL.list).context['object_list']
                self.assertTrue(
                    (self.note in object_list) is value)

    def test_client_contains_form(self):
        """Проверка формы."""
        for url in (URL.add, URL.edit):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context['form'],
                    NoteForm)
