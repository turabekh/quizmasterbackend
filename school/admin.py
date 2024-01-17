from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html
from .models import (
    Course, CourseInstance, 
    Topic, Quiz, Question, 
    Answer, QuizAttempt,
    StudentAnswer,
    QuestionFeedback,
    TopicTextTask,
)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Provide 4 empty fields for answers by default

class QuestionInline(admin.StackedInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1  # Provide 1 empty field for question by default

class QuizInline(admin.StackedInline):
    model = Quiz
    inlines = [QuestionInline]
    extra = 1  # Provide 1 empty field for quiz by default

class TopicAdmin(admin.ModelAdmin):
    inlines = [QuizInline]
    list_display = ('title', 'course')
    list_filter = ('course',)

class TopicInline(admin.StackedInline):
    model = Topic
    extra = 1  # Provide 1 empty field for topic by default

class CourseAdmin(admin.ModelAdmin):
    inlines = [TopicInline]
    list_display = ('title',)
    search_fields = ('title',)

class CourseInstanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'year', 'semester')
    list_filter = ('course', 'year', 'semester')
    filter_horizontal = ('students', 'instructors')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    list_filter = ('quiz',)
    inlines = [AnswerInline]

class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'question', 'selected_answer', 'is_correct')
    list_filter = ('quiz_attempt__student', 'quiz_attempt' )

    @admin.display(description='Student')
    def get_student(self, obj):
        return obj.quiz_attempt.student

    @admin.display(description='Is Correct')
    def is_correct(self, obj):
        if obj.selected_answer.is_correct:
            return format_html('<span style="color: green;">Correct</span>')
        else:
            return format_html('<span style="color: red;">Incorrect</span>')

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'attempt_time')
    list_filter = ('student__group', 'student', 'quiz')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)\
            .select_related('student', 'quiz')\
            .order_by('-attempt_time') \
            .order_by('-score') \
            .prefetch_related('student_answers__selected_answer')

        return queryset
    
class QuestionFeedbackAdmin(admin.ModelAdmin):
    list_display = ('question', 'student', 'text')
    list_filter = ('question', 'student')

class TopicTextTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic')
    list_filter = ('topic',)

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseInstance, CourseInstanceAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Quiz)  # Quiz is managed through TopicAdmin
admin.site.register(Question, QuestionAdmin)  # Question is managed through QuizInline
admin.site.register(Answer)    # Answer is managed through AnswerInline
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.register(QuestionFeedback, QuestionFeedbackAdmin)
admin.site.register(TopicTextTask, TopicTextTaskAdmin)
