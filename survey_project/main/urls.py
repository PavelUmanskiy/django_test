from django.urls import path

from .views import index_view, surveys_view, survey_view

urlpatterns = [
    path('', index_view, name='index'),
    path('surveys/', surveys_view, name='surveys'),
    path('surveys/<int:pk>/', survey_view, name='survey')
]