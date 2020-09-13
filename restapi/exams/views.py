import datetime

from django.http import JsonResponse, HttpResponse

from .models import ExamTemplate, ExamEvent
from .serializers import ExamTemplateSerializer, ExamEventSerializer

# Create your views here.

# id users od 1
USERS = ['admin', 'egzaminator', 'egzaminator2', 'egzaminator3', 'egzaminator4', 'uczestnik',  'uczestnik2',
         'uczestnik3', 'uczestnik4', 'uczestnik5']
GROUPS = ['Administrator', 'Examiner', 'Participant']

logged_in_user_id = '2'
logged_in_user_group = GROUPS[1]


def get_exam_event_first(request, whoami):
    exam_event = None
    if logged_in_user_group == 'Administrator' or logged_in_user_group == 'Examiner':
        if whoami == 'organizer':
            exam_event = ExamEvent.objects.filter(organizer=logged_in_user_id)
        elif whoami == 'examiner':
            exam_event = ExamEvent.objects.filter(examiners=logged_in_user_id)
    else:
        return HttpResponse('Brak dostępu')
    serializer = ExamEventSerializer(exam_event, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_exam_event_second(request, which_exams):
    today = datetime.date.today()
    exam_event = None
    if logged_in_user_group == 'Participant':
        if which_exams == 'past':
            exam_event = ExamEvent.objects.filter(date_exam__lt=today, participants=logged_in_user_id)
        elif which_exams == 'today':
            exam_event = ExamEvent.objects.filter(date_exam__contains=today, participants=logged_in_user_id)
        elif which_exams == 'future':
            exam_event = ExamEvent.objects.filter(date_exam__gt=today, participants=logged_in_user_id)
        elif which_exams == 'all':
            exam_event = ExamEvent.objects.filter(participants=logged_in_user_id)
    else:
        if which_exams == 'past':
            exam_event = ExamEvent.objects.filter(date_exam__lt=today)
        elif which_exams == 'today':
            exam_event = ExamEvent.objects.filter(date_exam__contains=today)
        elif which_exams == 'future':
            exam_event = ExamEvent.objects.filter(date_exam__gt=today)
        elif which_exams == 'all':
            exam_event = ExamEvent.objects.all()
    serializer = ExamEventSerializer(exam_event, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_exam_template_all(request):
    exam = ExamTemplate.objects.all()
    serializer = ExamTemplateSerializer(exam, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_exam_template_object(request, id):
    exam = ExamTemplate.objects.filter(id=id)
    serializer = ExamTemplateSerializer(exam, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_result_exam(reguest):
    exam = ExamEvent.objects.filter(participants=logged_in_user_id)
    serializer = ExamEventSerializer(exam, many=True)
    return JsonResponse(serializer.data, safe=False)
