# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import Question
# Create your tests here.

class QeustionMethodTests(TestCase):
    def test_was_published_recently_with_futrue_question(self):
        time = timezone.now() + datetime.timedelta(days=1)
        futrue_question = Question(pub_date=time)
        self.assertEqual(futrue_question.was_published_recently(), False)
    def test_was_pubulished_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)
    def test_was_published_recently_with_recently_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        #print("****",time, timezone.now())
        recently_question = Question(pub_date=time)
        self.assertEqual(recently_question.was_published_recently(), True)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QestionViewTest(TestCase):
    """
    If no questions exist, an appropriate message should be displayed.
    """
    def test_index_view_with_no_question(self):
        response = self.client.get(reverse('polls:polls_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Question with a pub_date in the past should be displayed on the index page.
        :return:
        """
        create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:polls_index'))
        #print('###', response.context['latest_question_list'])
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_index_view_with_a_futrue_question(self):
        """
        Question with a pub_date in the future should not be displayed on the index page.
        :return:
        """
        question = create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:polls_index'))
        self.assertContains(response, 'No polls are available',
                            status_code=200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions should be displayed.
        :return:
        """
        create_question(question_text='Future question', days=30)
        create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:polls_index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_index_view_with_two_past_question(self):
        """
        The questions index page may display multiple question.
        :return:
        """
        create_question(question_text='Past question 1', days=-30)
        create_question(question_text='Past question 2', days=-5)
        response = self.client.get(reverse("polls:polls_index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2>', '<Question: Past question 1>']
        )

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question', days=5)
        response = self.client.get(reverse("polls:polls_detail", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text='Past question', days=-5)
        response = self.client.get(reverse("polls:polls_detail", args=(past_question.id,)))
        self.assertEqual(response.status_code, 200)