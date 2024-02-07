from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Survey, Answer
from .utils.constants import HttpResponseCreated


def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


@login_required
def survey_list(request: HttpRequest) -> HttpResponse:
    query = """
    SELECT *
    FROM public.main_survey AS ms
    ORDER BY ms.last_update DESC
    """
    surveys = Survey.objects.raw(query)
    return render(request, 'surveys/surveys.html', {'surveys': surveys})

@login_required
def survey_detail(request: HttpRequest) -> HttpResponse:
    query = """
    SELECT *
    FROM public.main_survey AS ms
    JOIN public.main_question AS mq
        ON mq.survey_id = ms.id
    WHERE ms.id = %s
    """
    query_params = [request.GET.get('pk')]
    survey = Question.objects.raw(query, params=query_params)
    return render(request, 'surveys/survey.html', {'survey': survey})


@login_required
def answer_create(request: HttpRequest) -> HttpResponse:
    query = """
    INSERT INTO public.main_answer(respondent_id, question_id, answer_text)
    VALUES (%s, %s, %s)
    """
    respondent_id = request.GET.get('respondent_id', None)
    question_id = request.GET.get('question_id', None)
    answer_text = request.GET.get('answer_text', None)
    query_params = [respondent_id, question_id, answer_text]
    
    if not all(query_params):
        return HttpResponseBadRequest()
    
    created_answer = Answer.objects.raw(query, query_params)
    return HttpResponseCreated()