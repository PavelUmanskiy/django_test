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
    
    @property
    def total_answers(self) -> int:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                COUNT(ma.id)
            FROM public.main_answer AS ma
            JOIN public.main_question AS mq
                ON ma.question_id = mq.id
            JOIN public.main_survey AS ms
                ON mq.survey_id = ms.id
            """
            cursor.execute(query)
            answer_count = cursor.fetchone()[0]
            return answer_count


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
        on_delete=models.SET_NULL
    )
    question_text = models.TextField(max_length=2048)
    is_branching = models.BooleanField(default=False)  # Является вопросом с ветвлением
    depends_on = models.ForeignKey(  # Ссылка на ответ на вопрос с ветвлением
        to='Answer',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='branches'
    )
    dependency_condition = models.TextField(  # Условие ветвления
        max_length=2048,
        null=True,
        blank=True,
        default=None
    )

    def __str__(self) -> str:
        str_ = f'Question #{self.pk} of {self.survey}'
        return str_
    
    @property
    def total_answers(self) -> int:
        with connection.cursor() as cursor:
            query = """
            SELECT
                COUNT(ma.id)
            FROM public.main_answer AS ma
            JOIN public.main_question AS mq
                ON ma.question_id = mq.id
            """
            cursor.execute(query)
            answer_count = cursor.fetchone()[0]
            return answer_count


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
    
