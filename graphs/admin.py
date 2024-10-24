from django.contrib import admin

from graphs.models import Graph


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    pass
