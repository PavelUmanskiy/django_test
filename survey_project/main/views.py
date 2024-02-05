from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Question, Answer


@login_required
def index_view(request: HttpRequest) -> HttpResponse:
    query = """
    SELECT *
    FROM public.main_question AS mq
    JOIN
    WHERE 
    """
    questions = Question.objects.raw()
    return render(request, 'template_name.html', {'questions': questions})
