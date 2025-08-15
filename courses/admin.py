# courses/admin.py
from django.contrib import admin
from .models import Lesson, Word

class WordInline(admin.TabularInline):
    model = Word
    extra = 1
    fields = ("german", "translation", "part_of_speech", "example", "example_translation")

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "created_at")
    list_filter = ("published",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [WordInline]

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("german", "translation", "part_of_speech", "lesson")
    list_filter = ("lesson", "part_of_speech")
    search_fields = ("german", "translation", "example", "example_translation")
