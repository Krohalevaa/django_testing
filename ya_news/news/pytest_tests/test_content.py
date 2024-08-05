import pytest
from news.forms import CommentForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse


User = get_user_model()
URL_HOME = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client, all_news, news):
    """Количество новостей на странице"""
    response = client.get(URL_HOME)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client):
    """Сортировка новостей"""
    response = client.get(URL_HOME)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, author_client, news, detail_url):
    """Сортировка комментариев"""
    response = client.get(detail_url)
    assert 'news' in response.context
    comment_set = response.context['news']
    comments_dates = [comm.created for comm in comment_set.comment_set.all()]
    assert comments_dates == sorted(comments_dates)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, detail_url):
    """Анонимному пользователю недоступна форма для
    отправки комментария на странице отдельной новости.
    """
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, news, detail_url):
    """Авторизованному пользователю доступна форма для отправки
    комментария на странице отдельной новости
    """
    response = admin_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
