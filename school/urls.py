from django.urls import path
from .views import (
    ActiveCourseInstanceListView,
    ActiveQuizListView,
    QuestionByQuizListView,
    QuizAttemptByStudentListView,
    TakeQuizView,
    QuizAttemptByIdView,
    CanSubmitQuizView,
    HighestScoresView,
    QuestionFeedbackView,
    TextTaskRetrieveView,
    TopicsTextTaskListView,
)

urlpatterns = [
    # ... other URL patterns ...
    path('active-course-instances/', ActiveCourseInstanceListView.as_view(), name='active_course_instances'),
    path('active-quizzes/', ActiveQuizListView.as_view(), name='active_quizzes'),
    path('questions-by-quiz/<int:quiz_id>/', QuestionByQuizListView.as_view(), name='questions_by_topic'),
    path('quiz-attempts-by-student/', QuizAttemptByStudentListView.as_view(), name='quiz_attempts_by_student'),
    path('take-quiz/<int:quiz_id>/', TakeQuizView.as_view(), name='take_quiz'),
    path('quiz-attempt/<int:quiz_attempt_id>/', QuizAttemptByIdView.as_view(), name='quiz_attempt_by_id'),
    path('can-submit-quiz/<int:quiz_id>/', CanSubmitQuizView.as_view(), name='can_submit_quiz'),
    path('leaderboard/', HighestScoresView.as_view(), name='highest_scores'),
    path('question-feedback/', QuestionFeedbackView.as_view(), name='question_feedback'),
    path('topic-text-tasks/', TopicsTextTaskListView.as_view(), name='topic_text_tasks'),
    path('topic-text-tasks/<int:pk>/', TextTaskRetrieveView.as_view(), name='topic_text_task'),
]
