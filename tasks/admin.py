from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ['title', 'status', 'due_date', 'created_at']
    list_filter   = ['status']
    search_fields = ['title', 'description']
