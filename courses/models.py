# courses/models.py
from django.db import models
from django.utils.text import slugify

class Lesson(models.Model):
    title = models.CharField("Название урока", max_length=150)
    slug = models.SlugField("Слаг", max_length=160, unique=True, blank=True)
    description = models.TextField("Краткое описание", blank=True)
    published = models.BooleanField("Опубликован", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# класс для слов, связанных с уроками
class Word(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="words")
    german = models.CharField("Немецкое слово", max_length=120)
    translation = models.CharField("Перевод", max_length=200)

    part_of_speech = models.CharField("Часть речи", max_length=50, blank=True)
    example = models.CharField("Пример", max_length=250, blank=True)
    example_translation = models.CharField("Перевод примера", max_length=250, blank=True)

    class Meta:
        ordering = ["german"]
        verbose_name = "Слово"
        verbose_name_plural = "Слова"

    def __str__(self):
        return f"{self.german} — {self.translation}"