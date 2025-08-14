# courses/admin.py
from django.contrib import admin
from .models import Lesson, Word

class WordInline(admin.TabularInline):
    model = Word
    extra = 1

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "created_at")
    list_filter = ("published",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [WordInline]

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("german", "translation", "lesson")
    list_filter = ("lesson",)
    search_fields = ("german", "translation")
