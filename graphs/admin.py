from django.contrib import admin

from graphs.models import Dataset


@admin.register(Dataset)
class GraphAdmin(admin.ModelAdmin):
    pass
