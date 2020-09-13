from django.urls import path

from . import views

urlpatterns = [
    path('api/exam/event/first/<str:whoami>', views.get_exam_event_first),
    path('api/exam/event/second/<str:which_exams>', views.get_exam_event_second),
    path('api/exam/template/', views.get_exam_template_all),
    path('api/exam/template/<int:id>', views.get_exam_template_object),
    path('api/exam/results/', views.get_result_exam),
]
