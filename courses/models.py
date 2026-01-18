# courses/models.py
from django.db import models
from django.utils.text import slugify


class Lesson(models.Model):
    """
    Модель урока.
    Содержит основную информацию об уроке и указывает, какой шаблон использовать для отображения.
    """

    title = models.CharField("Название урока", max_length=150)
    slug = models.SlugField(
        "Слаг", max_length=160, unique=True, blank=True,
        help_text="Автоматически генерируется из названия, если не указать вручную."
    )
    description = models.TextField("Краткое описание", blank=True)

    # Определяем шаблон отображения (таблица, текст или кастомный вариант)
    TEMPLATE_CHOICES = [
        ("lesson_table.html", "С таблицей"),
        ("lesson_text.html", "Только текст"),
        ("lesson_custom.html", "Кастомный шаблон"),
    ]
    template_name = models.CharField(
        "Шаблон",
        max_length=100,
        choices=TEMPLATE_CHOICES,
        default="lesson_text.html"
    )

    published = models.BooleanField("Опубликован", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # последние уроки первыми
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        При сохранении автоматически создаём slug из названия,
        если он не был указан вручную.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Word(models.Model):
    """
    Модель слова, связанного с уроком.
    Хранит переводы, примеры и дополнительную информацию.
    """

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        related_name="words",
        verbose_name="Урок"
    )

    german = models.CharField("Немецкое слово", max_length=120)
    translation = models.CharField("Перевод", max_length=200)

    # Часть речи (лучше сделать choices, но пока оставим свободный ввод)
    part_of_speech = models.CharField("Часть речи", max_length=50, blank=True)

    # Пример использования и его перевод
    example = models.CharField("Пример", max_length=250, blank=True)
    example_translation = models.CharField("Перевод примера", max_length=250, blank=True)

    # Транскрипция (опционально)
    transcription = models.CharField("Транскрипция", max_length=250, blank=True)

    class Meta:
        ordering = ["german"]  # сортировка по алфавиту немецких слов
        verbose_name = "Слово"
        verbose_name_plural = "Слова"

    def __str__(self):
        return f"{self.german} — {self.translation}"


class QuizStat(models.Model):
    """Статистика по прохождению квизов для урока."""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="quiz_stats")
    correct_count = models.PositiveIntegerField("Правильных ответов")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Статистика квиза"
        verbose_name_plural = "Статистика квизов"

    def __str__(self):
        return f"{self.lesson.title}: {self.correct_count} @ {self.created_at:%Y-%m-%d %H:%M}"
