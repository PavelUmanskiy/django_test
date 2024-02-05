from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    next_question = models.ForeignKey(
        to='Question',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    question_text = models.TextField(max_length=2048)
    

class Answer(models.Model):
    respondent = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.SET_NULL
    )
    answer_text = models.TextField(max_length=2048)
    answer_date = models.DateField(auto_now=True)
    
