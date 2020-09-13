from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import models


# Create your models here.


class Result(models.Model):
    points = models.IntegerField()
    participants = models.OneToOneField(User, on_delete=models.CASCADE, default='')


class ExaminationTask(models.Model):
    content = models.TextField()
    maximum_points = models.IntegerField()
    results = models.ManyToManyField(Result, related_name="results", blank=True, default=None)


class ExamTemplate(models.Model):
    title = models.CharField(max_length=256)
    subjects = models.CharField(max_length=256)
    tasks = models.ManyToManyField(ExaminationTask, blank=True)


class ExamEvent(models.Model):
    date_exam = models.DateTimeField()
    place = models.CharField(max_length=128)
    published = models.BooleanField()
    exam = models.ForeignKey(ExamTemplate, on_delete=models.CASCADE, related_name='exam')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizer', blank=True, default=None,
                                  null=True)
    examiners = models.ManyToManyField(User, related_name='examiners', blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)


GROUPS = ['Administrator', 'Examiner', 'Participant']
MODELS = ['examination task', 'result', 'exam template', 'exam event']
PERMISSIONS = ['add', 'view']


class Command(BaseCommand):

    def handle(*args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    if group == 'Participant' and permission == 'add':
                        continue
                    name = 'Can {} {}'.format(permission, model)
                    model_add_perm = Permission.objects.get(name=name)
                    new_group.permissions.add(model_add_perm)


Command.handle()
