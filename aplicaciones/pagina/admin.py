from django.contrib import admin
from .models import Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'percent', 'updated')
    list_filter = ('course',)
    search_fields = ('user__username', 'course')
from django.contrib import admin

# Register your models here.
