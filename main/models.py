from django.contrib.auth.models import User
from django.db import models

from formMaker.helpers import generate_hash
from main.helpers import build_filename_with_hash


class Form(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(default=generate_hash, max_length=10)

    def number_of_answers(self):
        return AnonymousUser.objects.filter(answer__question__form=self).distinct().count()

    def get_sorted_question_set(self):
        return self.question_set.order_by('number')


class Question(models.Model):
    TYPE_CHOICES = (
        ('UNIQUE_ANSWER', 'unique answer'),
        ('MULTIPLE_ANSWER', 'multiple_answer'),
        ('TEXT', 'text'),
        ('HTML', 'html'),
        ('FILE', 'file')
    )
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPE_CHOICES, max_length=100)
    text = models.CharField(max_length=500)
    number = models.IntegerField()

    def get_anonymous_users(self):
        return AnonymousUser.objects.filter(answer__question=self).distinct()

    def get_sorted_possible_answer_set(self):
        return self.possibleanswer_set.order_by('number')


class PossibleAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    number = models.IntegerField()


class AnonymousUser(models.Model):
    """
    A model to keep track of answers of the same frontend session.
    """
    uuid = models.CharField(default=generate_hash, max_length=10, primary_key=True)

    def get_chosen_possible_answers(self):
        return PossibleAnswer.objects.filter(answer__author=self).distinct()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    chosenAnswer = models.ForeignKey(PossibleAnswer, null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    isHtml = models.BooleanField(default=False)
    file = models.FileField(upload_to=build_filename_with_hash, blank=True, null=True)

    author = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)
