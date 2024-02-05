from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    author = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    last_update = models.DateField(auto_now=True)
    description = models.TextField(max_length=2048)


class Question(models.Model):
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)
    next_question = models.ForeignKey(
        to='Question',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    question_text = models.TextField(max_length=2048)


class Answer(models.Model):
    respondent = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.SET_NULL
    )
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    answer_text = models.TextField(max_length=2048)
    last_update = models.DateField(auto_now=True)
    
