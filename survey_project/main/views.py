from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Question, Survey, Answer


def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


@login_required
def surveys_view(request: HttpRequest) -> HttpResponse:
    query = """
    SELECT *
    FROM public.main_survey AS ms
    ORDER BY ms.last_update DESC
    """
    surveys = Survey.objects.raw(query)
    return render(request, 'surveys/surveys.html', {'surveys': surveys})

@login_required
def survey_view(request: HttpRequest) -> HttpResponse:
    query = """
    SELECT *
    FROM public.main_question AS mq
    JOIN public.main_survey as ms
        ON mq.survey_id = ms.id
    WHERE ms.id = %s
    """
    query_params = [request.GET.get('pk')]
    questions = Question.objects.raw(query, params=query_params)
    return render(request, 'surveys/survey.html', {'questions': questions})
