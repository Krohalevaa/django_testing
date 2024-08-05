# from datetime import timedelta
import pytest
from news.forms import CommentForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
# from django.utils import timezone

from news.models import News, Comment

User = get_user_model()
URL_HOME = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client):
    """Количество новостей на странице"""
    all_news = [
        News(title=f'Новость {index}', text='Текст.')
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    response = client.get(URL_HOME)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client):
    """Сортировка новостей"""
    response = client.get(URL_HOME)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(author, author_client, news):
    """Сортировка комментариев"""
    response = author_client.get(reverse('news:detail', args=(news.id,)))
    assert 'news' in response.context
    comment_list = response.context['news']
    comments_dates = [comm.created for comm in comment_list.comment_set.all()]
    assert comments_dates == sorted(comments_dates)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, detail_url):
    """Анонимному пользователю недоступна форма для
    отправки комментария на странице отдельной новости.
    """
    response = client.get(detail_url)
    assert 'form' not in response.context
