from django.contrib import admin
from .models import ExamTemplate, ExamEvent, ExaminationTask, Result
# Register your models here.

admin.site.register(ExamTemplate)
admin.site.register(ExamEvent)
admin.site.register(ExaminationTask)
admin.site.register(Result)


