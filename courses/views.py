# courses/views.py
from django.shortcuts import render, get_object_or_404
from .models import Lesson
from django.utils import timezone

def home(request):
    latest = Lesson.objects.filter(published=True)[:5]
    return render(request, "courses/home.html", {"latest": latest, "now": timezone.now()})

def lesson_list(request):
    lessons = Lesson.objects.filter(published=True)
    return render(request, "courses/lesson_list.html", {"lessons": lessons})

def lesson_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug, published=True)
    # благодаря related_name="words" доступно lesson.words.all()
    return render(request, "courses/lesson_detail.html", {"lesson": lesson})
