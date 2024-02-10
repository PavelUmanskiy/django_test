from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, Http404
from django.contrib.auth.decorators import login_required
from django.db import connection

from .models import Question, Survey, Answer
from .utils.constants import EXCESS_AUTHOR_FIELDS
from .utils.queries import QUESTION_STATS_QUERY
from .utils.data_processing import reorganize_question_stats


def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {'user': request.user})


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
    questions = (
        Question.objects
        .all()
        .prefetch_related(
            'survey',
            'depends_on',
            'answers',
            'answers__respondent'
        )
        .filter(survey=None)
        .exclude(answers__respondent__id=request.user.id)
        .defer(
            'next_question',
            'is_branching',
            'depends_on',
        )
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
    
    question = Question.objects\
        .filter(pk=int(question_id)).prefetch_related('survey')[0]
    new_answer = Answer.objects.create(
        respondent=request.user,
        question=question,
        answer_text=answer_text,
    )
    
    context = {'question': question, 'answer': new_answer}
    if question.next_question is not None:
        context['next_question'] = question.next_question

    elif question.is_branching:
        next_branch = None
        branches = question.branches.all()
        for branch in branches:
            if question.is_choices:
                if (
                    new_answer.answer_text.strip() == 
                    question.right_answer.strip()
                ):
                    next_branch = branch
                    break
            else:
                if (
                    new_answer.answer_text.strip() == 
                    branch.right_answer.strip()
                ):
                    next_branch = branch
                    break
        if next_branch is None:
            context['next_question'] = question.default_branch
        else:
            context['next_question'] = next_branch
    
    return render(request, 'questions/next_question_button.html', context)


@login_required
def survey_stats(request: HttpRequest, pk: int) -> HttpResponse:
    context = {'survey_id': pk}
    with connection.cursor() as cursor:
        cursor.execute(QUESTION_STATS_QUERY, {'survey_id': pk})
        rows = cursor.fetchall()
    stats = reorganize_question_stats(rows)
    context['survey_stats'] = stats
    return render(request, 'surveys/survey_stats.html', context)
