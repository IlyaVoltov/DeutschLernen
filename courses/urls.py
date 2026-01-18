# courses/urls.py
from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.home, name="home"),
    path("lessons/", views.lesson_list, name="lesson_list"),
    path("lessons/<slug:slug>/", views.lesson_detail, name="lesson_detail"),
    path('<slug:slug>/quiz/', views.lesson_quiz, name='lesson_quiz'),
    path('<slug:slug>/example-quiz/', views.lesson_example_quiz, name='lesson_example_quiz'),
    path('<slug:slug>/quiz/record/', views.record_quiz_stat, name='record_quiz_stat'),
    path('<slug:slug>/quiz/stats/', views.quiz_stats, name='quiz_stats'),
    # другие маршруты для приложения
]
