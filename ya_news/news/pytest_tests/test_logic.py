import pytest
from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING

FORM_DATA = {'text': 'Новый текст'}


@pytest.mark.django_db
def test_user_can_comment(author_client, author, news):
    """Авторизованный пользователь может комментировать"""
    comments_count_before = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=FORM_DATA)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == comments_count_before + 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_comment(client, news):
    """Анонимный пользователь не может комментировать"""
    comments_count_before = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=FORM_DATA)
    assert Comment.objects.count() == comments_count_before


@pytest.mark.django_db
def test_cant_use_bad_words(author_client, news,):
    """Проверка комментариев на содержание запрещенных слов"""
    comments_count_before = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == comments_count_before


def test_edit_comment(author_client, news, comment):
    """Пользователь может редактировать свой комментарий"""
    edit_url = reverse('news:edit', args=(comment.id,))
    news_url = reverse('news:detail', args=(news.id,))
    url_to_comments = news_url + '#comments'
    response = author_client.post(edit_url, data=FORM_DATA)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == FORM_DATA['text']


@pytest.mark.django_db
def test_delete_comment(author_client, news, comment):
    """Пользователь может удалять свой комментарий"""
    comments_count_before = Comment.objects.count()
    delete_url = reverse('news:delete', args=(comment.id,))
    news_url = reverse('news:detail', args=(news.id,))
    url_to_comments = news_url + '#comments'
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == comments_count_before - 1


def test_user_cant_edit_other_comment(
        not_author_client, comment
):
    """Пользователь не может редактировать чужой комментарий"""
    edit_url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(edit_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Комментарий'


@pytest.mark.django_db
def test_user_cant_delete_other_comment(not_author_client, comment):
    """Пользователь не может удалять чужой комментарий"""
    comments_count_before = Comment.objects.count()
    delete_url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count_before
