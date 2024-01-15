import random
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max, F
from django.shortcuts import get_object_or_404
from .models import (
    CourseInstance, 
    Course,
    Quiz,
    Question,
    QuizAttempt,
    Answer,
    StudentAnswer,
    TopicTextTask,
    Topic,
)
from .serializers import (
    CourseInstanceWithTopicsSerializer,
    QuizSerializer,
    QuestionSerializer,
    QuizAttemptSerializer,
    QuestionFeedbackSerializer,
    TopicTextTaskSerializer,
    TextTaskSerializer,
    
)

class ActiveCourseInstanceListView(APIView):
    
    permission_classes = [IsAuthenticated]  # Only logged-in users can access this view
    
    def get(self, request):
        # Assuming 'is_active' is a field in your Course model
        active_courses = Course.objects.filter(is_active=True)
        course_instances = CourseInstance.objects.filter(course__in=active_courses)
        serializer = CourseInstanceWithTopicsSerializer(course_instances, many=True)
        return Response(serializer.data)
    
class ActiveQuizListView(APIView):

    permission_classes = [IsAuthenticated]  # Only logged-in users can access this view

    def get(self, request):
        # Assuming 'is_active' is a field in your Quiz model
        active_quizzes = Quiz.objects.order_by("id")
        serializer = QuizSerializer(active_quizzes, many=True)
        return Response(serializer.data)
    
class QuestionByQuizListView(APIView):

    permission_classes = [IsAuthenticated]  # Only logged-in users can access this view

    def get(self, request, quiz_id):
        # Assuming 'topic' is a field in your Question model
        questions = Question.objects.filter(quiz=quiz_id)
        serializer = QuestionSerializer(questions, many=True)
        data = serializer.data
        # shuffle the questions
        random.shuffle(data)
        return Response(data)

class TakeQuizView(APIView):

    permission_classes = [IsAuthenticated]  # Only logged-in users can access this view

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        student = request.user  # Assuming the student is the logged-in user
        # Check the number of attempts
        attempts = QuizAttempt.objects.filter(student=student, quiz=quiz).count()
        max_attempts = 3  # Set your limit here

        if attempts >= max_attempts:
            return Response({"message": "You have reached the maximum number of attempts for this quiz."}, status=400)
        
        # Extract submitted answers
        submitted_answers = request.data.get('answers')  # Format: [{'question_id': x, 'answer_id': y}, ...]

        # Create a new QuizAttempt
        quiz_attempt = QuizAttempt.objects.create(student=student, quiz=quiz, score=0)

        correct_answers_count = 0

        for answer_data in submitted_answers:
            question = get_object_or_404(Question, pk=answer_data['question_id'])
            selected_answer = get_object_or_404(Answer, pk=answer_data['answer_id'])

            # Record the student's answer
            StudentAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                question=question,
                selected_answer=selected_answer
            )

            # Check if the answer is correct
            if selected_answer.is_correct:
                correct_answers_count += 1

        # Calculate the score
        total_questions = len(quiz.questions.all())
        score = (correct_answers_count / total_questions) * 100
        quiz_attempt.score = score
        quiz_attempt.save()

        return Response({
            "message": "Quiz attempt recorded.",
            "score": score,
            "correct_answers_count": correct_answers_count,
            "total_questions": total_questions
        })
    
class QuizAttemptByStudentListView(APIView):

    permission_classes = [IsAuthenticated]  # Only logged-in users can access this view
    
    def get(self, request):
        student = request.user  # Assuming the student is the logged-in user
        quiz_attempts = QuizAttempt.objects.filter(student=student)
        serializer = QuizAttemptSerializer(quiz_attempts, many=True)
        return Response(serializer.data)

class QuizAttemptByIdView(APIView):

    permission_classes = [IsAuthenticated]  # Only logged-in users can access this view

    def get(self, request, quiz_attempt_id):
        user = request.user
        quiz_attempt = get_object_or_404(QuizAttempt, pk=quiz_attempt_id, student=user)
        serializer = QuizAttemptSerializer(quiz_attempt)
        return Response(serializer.data)
    
class CanSubmitQuizView(APIView):

    permission_classes = [IsAuthenticated]  # Only logged-in users can access this view

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        student = request.user  # Assuming the student is the logged-in user
        # Check the number of attempts
        attempts = QuizAttempt.objects.filter(student=student, quiz=quiz).count()
        max_attempts = 3  # Set your limit here

        if attempts >= max_attempts:
            return Response({"message": "You have reached the maximum number of attempts for this quiz."}, status=400)
        
        return Response({"message": "You can submit the quiz."}, status=200)
    
class HighestScoresView(APIView):
    def get(self, request):
        # Get the highest score for each quiz
        highest_scores = QuizAttempt.objects.values('quiz_id').annotate(
            highest_score=Max('score'),
            student_email=F('student__email'), 
            student_first_name=F('student__first_name'),
            student_last_name=F('student__last_name')
        )

        # Get the list of quizzes
        quizzes = Quiz.objects.filter(id__in=[score['quiz_id'] for score in highest_scores])
        
        # Prepare the response data
        response_data = []
        for quiz in quizzes:
            score_data = max([score for score in highest_scores if score['quiz_id'] == quiz.id], key=lambda x: x['highest_score'])
            response_data.append({
                'id': quiz.id,
                'title': quiz.title,
                'highest_score': score_data.get('highest_score'),
                'student_email': score_data.get('student_email'), 
                'student_first_name': score_data.get('student_first_name'),
                'student_last_name': score_data.get('student_last_name'),
            })

        return Response(response_data)
    
class QuestionFeedbackView(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        data['student'] = user.id
        serializer = QuestionFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Question feedback recorded."}, status=200)
        else:
            return Response(serializer.errors, status=400)

class TextTaskRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can access this view
    queryset = TopicTextTask.objects.all()
    serializer_class = TextTaskSerializer

class TopicsTextTaskListView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can access this view
    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicTextTaskSerializer(topics, many=True)
        return Response(serializer.data)