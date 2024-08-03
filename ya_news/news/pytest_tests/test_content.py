import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm

URL_HOME = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client, all_news):
    """Ограничение по количеству новостей на главной"""
    response = client.get(URL_HOME)
    news = response.context['object_list']
    news_count = news.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, all_news):
    """Сортировка новостей"""
    response = client.get(URL_HOME)
    news = response.context['object_list']
    all_dates = [one_news.date for one_news in news]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news, comments, detail_url):
    """Сортировка комментариев"""
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = [
        one_comment.created for one_comment in news.comment_set.all()
    ]
    sorted_comments = sorted(all_comments)
    assert all_comments == sorted_comments


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news, detail_url):
    """Анонимному пользователю недоступна форма для комментария"""
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, news, detail_url):
    """Авторизованному пользователю доступна форма для комментария"""
    response = admin_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
