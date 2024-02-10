from django.db import models, connection
from django.contrib.auth.models import User


class Survey(models.Model):
    author = models.ForeignKey(
        to=User,
        null=True,
        default=None,
        on_delete=models.SET_NULL        
    )
    last_update = models.DateField(auto_now=True)
    description = models.TextField(max_length=2048)
    first_question = models.ForeignKey(
        to='Question',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='related_survey'
    )
 
    def __str__(self) -> str:
        str_ = f'Survey #{self.pk} by {self.author.username}'
        return str_


class Question(models.Model):
    survey = models.ForeignKey(
        to=Survey,
        null=True,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    next_question = models.ForeignKey(
        to='Question',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='previous_question'
    )
    is_choices = models.BooleanField(default=False)
    choices = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        default=None
    )
    question_text = models.TextField(
        max_length=2048,
        null=True,
        blank=True,
        default=None
    )
    is_branching = models.BooleanField(default=False)  # Является вопросом с ветвлением
    depends_on = models.ForeignKey(  # Ссылка на вопрос с ветвлением
        to='Question',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='branches'
    )
    right_answer = models.TextField(  # Условие ветвления, если выполнено - переход на next_question
        max_length=2048,
        null=True,
        blank=True,
        default=None
    )
    default_branch = models.ForeignKey(  # Если условие не выполнено - переход на этот вопрос.
        to='Question',                   # Если он NULL, опрос закончен
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='wrongly_answered_question'
    )

    def __str__(self) -> str:
        str_ = f'Question #{self.pk} of {self.survey}'
        return str_


class Answer(models.Model):
    respondent = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.SET_NULL
    )
    question = models.ForeignKey(
        to=Question,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer_text = models.TextField(max_length=2048)
    last_update = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        respondent = self.respondent.username
        str_ = f'Answer #{self.pk} by {respondent} on {self.question}'
        return str_
    
