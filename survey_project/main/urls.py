from django.urls import path

from .views import (
    index_view,
    survey_list,
    survey_detail,
    question_list,
    question_detail,
    answer_create,
)

urlpatterns = [
    path('', index_view, name='index'),
    path('surveys/', survey_list, name='surveys'),
    path('surveys/<int:pk>/', survey_detail, name='survey'),
    path('questions/', question_list, name='questions'),
    path('questions/<int:pk>/', question_detail, name='question'),
    path('answers/create/', answer_create, name='new_answer'),
]