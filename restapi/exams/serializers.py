from rest_framework import serializers
from .models import ExamTemplate, ExamEvent, ExaminationTask, Result
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ResultSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=False)

    class Meta:
        model = Result
        fields = ('id', 'points', 'participants')


class ExaminationTaskSerializer(serializers.ModelSerializer):
    results = ResultSerializer(many=True)

    class Meta:
        model = ExaminationTask
        fields = ('id', 'content', 'maximum_points', 'results')


class ExamTemplateSerializer(serializers.ModelSerializer):
    tasks = ExaminationTaskSerializer(many=True)

    class Meta:
        model = ExamTemplate
        fields = ('id', 'title', 'subjects', 'tasks')


class ExamEventSerializer(serializers.ModelSerializer):
    exam = ExamTemplateSerializer(many=False)
    organizer = UserSerializer(many=False)
    examiners = UserSerializer(many=True)
    participants = UserSerializer(many=True)

    class Meta:
        model = ExamEvent
        fields = ('id', 'date_exam', 'place', 'published', 'exam', 'organizer', 'examiners', 'participants')

