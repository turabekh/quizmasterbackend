from rest_framework import serializers
from .models import (
    CourseInstance, Topic, 
    Quiz, Question, Answer,
    StudentAnswer, QuizAttempt,
    QuestionFeedback,
    TopicTextTask,
)

class CourseInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInstance
        fields = ['id', 'course', 'year', 'semester', 'students', 'instructors']
        # You can adjust the fields based on what information you want to include

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Topic
        fields = ['id', 'title', 'quizzes']
        # You can adjust the fields based on what information you want to include

class CourseInstanceWithTopicsSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = CourseInstance
        fields = ['id', 'course', 'year', 'semester', 'topics']

    def get_topics(self, obj):
        topics = Topic.objects.filter(course=obj.course)
        serializer = TopicSerializer(topics, many=True)
        return serializer.data

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']
        # You can adjust the fields based on what information you want to include

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = Question
        fields = ['id', 'text', 'answers']
        # You can adjust the fields based on what information you want to include
 
    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj)
        serializer = AnswerSerializer(answers, many=True)
        return serializer.data
    
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'is_active']
        # You can adjust the fields based on what information you want to include

class StudentAnswerSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    question_text = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentAnswer
        fields = ['id', 'selected_answer', 'question_text', "is_correct", "text"]

    def get_text(self, obj):
        return obj.selected_answer.text
    
    def get_question_text(self, obj):
        return obj.question.text

        # You can adjust the fields based on what information you want to include

class QuizAttemptSerializer(serializers.ModelSerializer):
    student_answers = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = QuizAttempt
        fields = ['id', 'quiz', 'student_answers', 'attempt_time', 'score']
        # You can adjust the fields based on what information you want to include

    def get_student_answers(self, obj):
        student_answers = StudentAnswer.objects.filter(quiz_attempt=obj)
        serializer = StudentAnswerSerializer(student_answers, many=True)
        return serializer.data
    
class HighestScoreSerializer(serializers.ModelSerializer):
    highest_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    student_email = serializers.EmailField()

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'highest_score', 'student_email',)

class QuestionFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionFeedback
        fields = ['id', 'question', 'student', 'text']
        # You can adjust the fields based on what information you want to include

class TextTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicTextTask
        fields = ['id', 'title', 'content']
        # You can adjust the fields based on what information you want to include

class TopicTextTaskSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = Topic
        fields = ['id', 'title', 'tasks']

    def get_tasks(self, obj):
        tasks = TopicTextTask.objects.filter(topic=obj)
        serializer = TextTaskSerializer(tasks, many=True)
        return serializer.data

