from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, Http404
from django.contrib.auth.decorators import login_required

from .models import Question, Survey, Answer
from .utils.classes import HttpResponseCreated
from .utils.constants import EXCESS_AUTHOR_FIELDS


def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


@login_required
def survey_list(request: HttpRequest) -> HttpResponse:
    surveys = Survey.objects.all().prefetch_related('author', 'first_question')\
        .defer(*EXCESS_AUTHOR_FIELDS).order_by('-id')
    return render(request, 'surveys/surveys.html', {'surveys': surveys})


@login_required
def survey_detail(request: HttpRequest, pk: int) -> HttpResponse:
    survey = Survey.objects.all().prefetch_related('author', 'first_question')\
        .defer(*EXCESS_AUTHOR_FIELDS).filter(pk=pk)[0]
    if not survey:
        raise Http404()
    return render(request, 'surveys/survey.html', {'survey': survey})


@login_required
def question_list(request: HttpRequest):
    # TODO: Убедится что это оптимальный запрос
    questions = Question.objects.all().prefetch_related('survey', 'depends_on')\
        .filter(survey=None).defer(
            'next_question',
            'is_branching',
            'depends_on',
            'dependency_condition'
        )
    return render(request, 'questions/questions.html', {'questions': questions})


@login_required
def question_detail(request: HttpRequest, pk):
    question = Question.objects.all().prefetch_related('survey', 'depends_on')\
        .filter(pk=pk)[0]
    if not question:
        raise Http404()
    return render(request, 'questions/question.html', {'question': question})


@login_required
def answer_create(request: HttpRequest) -> HttpResponse:
    answer_text = request.POST.get('answer_text', None) 
    question_id = request.POST.get('question_id', None)
    if not answer_text or not question_id:
        return HttpResponseBadRequest()
    question = Question.objects.get(pk=int(question_id))
    created_answer = Answer.objects.create(
        respondent=request.user,
        question=question,
        answer_text=answer_text,
    )
    return render(request, 'questions/question_stats.html')