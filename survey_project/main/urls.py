from django.urls import path

from .views import index_view, survey_list, survey_detail

urlpatterns = [
    path('', index_view, name='index'),
    path('surveys/', survey_list, name='surveys'),
    path('surveys/<int:pk>/', survey_detail, name='survey')
]