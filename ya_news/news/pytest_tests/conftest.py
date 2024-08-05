import pytest

from news.models import Comment, News
from datetime import timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.test import Client
from pytest_lazyfixture import lazy_fixture

from news.models import Comment, News

from collections import namedtuple

COMMENTS_COUNT = 3
ADMIN = lazy_fixture('admin_client')
AUTHOR = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')

PK = 1

URL_NAME = namedtuple(
    'URL_NAME',
    [
        'home',
        'detail',
        'edit',
        'delete',
        'login',
        'logout',
        'signup',
    ],
)

URL = URL_NAME(
    reverse('news:home'),
    reverse('news:detail', args=(PK,)),
    reverse('news:edit', args=(PK,)),
    reverse('news:delete', args=(PK,)),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)


# Пользователи
@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


# Клиенты
@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


# Данные
@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def all_news():
    all_news = [
        News(title=f'Новость {index}', text='Текст.')
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def pk_for_args(news):
    return news.pk,


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        text='Комментарий',
        author=author
    )


@pytest.fixture
def comments(author, news):
    now = timezone.now()
    for index in range(COMMENTS_COUNT):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment_data(news, author):
    return {
        'text': 'Обновлённый комментарий',
        'news': news,
        'author': author
    }


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.pk,))
