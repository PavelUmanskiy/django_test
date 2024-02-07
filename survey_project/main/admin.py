from django.contrib import admin

from .models import Survey, Question, Answer


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'total_answers',
        'last_update',
        'description',
        'first_question'
    )
    list_display_links = ('id', 'first_question')
    search_fields = ('author__username', 'description')
    list_editable = ('author', 'description')
    list_filter = ('last_update', 'author')
    list_select_related = ('author', 'first_question')
    # ordering = ('-total_answers',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'survey',
        'total_answers',
        'next_question',
        'question_text',
        'is_branching',
        'depends_on',
        'dependency_condition',
    )
    list_display_links = ('id',)
    search_fields = ('question_text', 'dependency_condition')
    list_editable = (
        'next_question',
        'question_text',
        'is_branching',
        'depends_on',
        'dependency_condition',
    )
    list_filter = ('is_branching',)
    list_select_related = ('survey', 'depends_on')
    
        