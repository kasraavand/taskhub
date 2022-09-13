from django.contrib import admin
from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "done", "date_created")
    list_filter = ("done", "date_created")


admin.site.register(Task, TaskAdmin)

