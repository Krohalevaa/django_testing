from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import Client, TestCase
from django.urls import reverse
from notes.constance import NOTES_LIST
from notes.models import Note
from notes.forms import NoteForm
User = get_user_model()


class TestContentPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.user_client = Client()
        cls.user_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='i_5',
            author=cls.author
        )
        # cls.author = User.objects.create(username='Автор')
        # cls.note = Note.objects.create(
        #     title='Заголовок',
        #     text='Текст',
        #     author=cls.author,
        # )
        # cls.add_url = reverse('notes:add')
        # # cls.list_url = reverse('notes:list')
        # cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))

    def test_note_in_list_for_author(self):
        """Отдельная заметка передаётся на страницу со списком заметок"""
        # self.client.force_login(self.author)
        # response = self.client.get(NOTES_LIST)
        # object_list = response.context['object_list']
        # self.assertIn(self.note, object_list)
        response = self.user_client.get(NOTES_LIST)
        notes_count = response.context['object_list'].count()
        self.assertEqual(notes_count, 1)

    def test_note_not_in_list_for_another_user(self):
        """В списке заметок одного пользователя нет заметок другого"""
        # self.client.force_login(self.author)
        # self.user_client.force_login(self.reader)
        # response = self.client.get(NOTES_LIST)
        # object_list = response.context['object_list']
        # self.assertNotIn('note', object_list)
        self.user_client.force_login(self.reader)
        response = self.user_client.get(NOTES_LIST)
        notes_count = response.context['object_list'].count()
        self.assertEqual(notes_count, 0)

    def test_authorized_client_has_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for url, args in urls:
            with self.subTest(url=url):
                response = self.user_client.get(reverse(url, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
