# courses/views.py
from django.shortcuts import render, get_object_or_404
from .models import Lesson, Word
from django.utils import timezone
import random

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

# функция для теста на знание слов из урока
def lesson_quiz(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug, published=True)
    words = list(lesson.words.all())
    if len(words) < 2:
        return render(request, "courses/lesson_quiz.html", {"lesson": lesson, "error": "Недостаточно слов для теста."})
    selected = random.sample(words, 2)
    correct_word = random.choice(selected)
    return render(request, "courses/lesson_quiz.html", {
        "lesson": lesson,
        "words": words,
        "correct": correct_word
    })

# функция для теста перевода примера
def lesson_example_quiz(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug, published=True)
    words = list(lesson.words.exclude(example="", example_translation=""))
    if not words:
        return render(request, "courses/lesson_example_quiz.html", {"lesson": lesson, "error": "Нет примеров для теста."})
    word = random.choice(words)
    return render(request, "courses/lesson_example_quiz.html", {
        "lesson": lesson,
        "word": word,
    })