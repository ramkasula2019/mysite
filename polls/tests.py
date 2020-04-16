import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question
# Create your tests here.

def create_question(question_text, days):
    time = timezone.now()+ datetime.timedelta(days=days)
    return  Question.objects.create(question_text = question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        If no question exist appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        """
        question with publication date in the past are displayedd in index page
        """
        create_question(question_text="Past question", days=-30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question>'])

    def test_future_question(self):
        """
        Question with pub_date in future are not displayed in index page
        """
        create_question(question_text="Future question", days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        """
        if future and past pub are available only past question are shown in index page
        """
        create_question(question_text="Future question", days=30)
        create_question(question_text="Past question", days=-30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question>'])

    def test_past_two_questoin(self):
        """
        if two past question are available both should be displayed in index
        """
        create_question(question_text="Past question 1", days=-24)
        create_question(question_text="Past question 2", days=-5)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2>', '<Question: Past question 1>'])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 not found.
        """
        future_question = create_question(question_text="Future question", days=20)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past question', days = -5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_futue_question(self):
        time = timezone.now()+ datetime.timedelta(days = 30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = old_time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        recent_time = timezone.now() - datetime.timedelta(hours=23,minutes=59, seconds=1)
        recent_question = Question(pub_date = recent_time)
        self.assertIs(recent_question.was_published_recently(), True)