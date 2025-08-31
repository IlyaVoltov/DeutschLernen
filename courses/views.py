# courses/views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Lesson
import random


def home(request):
    """
    Главная страница.
    Показывает последние 5 опубликованных уроков.
    """
    latest = Lesson.objects.filter(published=True)[:5]
    return render(
        request,
        "courses/home.html",
        {
            "latest": latest,
            "now": timezone.now(),  # можно использовать в шаблоне (например: {{ now }})
        }
    )


def lesson_list(request):
    """
    Список всех опубликованных уроков.
    """
    lessons = Lesson.objects.filter(published=True)
    return render(request, "courses/lesson_list.html", {"lessons": lessons})


def lesson_detail(request, slug):
    """
    Страница конкретного урока.
    Использует шаблон, указанный в поле Lesson.template_name.
    Благодаря related_name="words" можно обращаться: lesson.words.all()
    """
    lesson = get_object_or_404(Lesson, slug=slug, published=True)

    # ВАЖНО: теперь шаблон берётся из базы (lesson.template_name),
    # а не всегда lesson_detail.html
    return render(request, f"courses/{lesson.template_name}", {"lesson": lesson})


def lesson_quiz(request, slug):
    """
    Тест по словам из урока:
    - случайным образом выбираем 2 слова
    - одно из них будет правильным ответом
    """
    lesson = get_object_or_404(Lesson, slug=slug, published=True)
    words = list(lesson.words.all())

    # Проверка: нужно хотя бы 2 слова для теста
    if len(words) < 2:
        return render(request, "courses/lesson_quiz.html", {
            "lesson": lesson,
            "error": "Недостаточно слов для теста."
        })

    # Случайные два слова и правильный ответ
    selected = random.sample(words, 2)
    correct_word = random.choice(selected)

    return render(request, "courses/lesson_quiz.html", {
        "lesson": lesson,
        "words": words,
        "correct": correct_word,
    })


def lesson_example_quiz(request, slug):
    """
    Тест на перевод примеров:
    - выбираем случайное слово с заполненным example и example_translation
    """
    lesson = get_object_or_404(Lesson, slug=slug, published=True)

    # исключаем слова без примеров
    words = list(lesson.words.exclude(example="", example_translation=""))

    if not words:
        return render(request, "courses/lesson_example_quiz.html", {
            "lesson": lesson,
            "error": "Нет примеров для теста."
        })

    word = random.choice(words)

    return render(request, "courses/lesson_example_quiz.html", {
        "lesson": lesson,
        "word": word,
    })
