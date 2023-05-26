from django.contrib import admin

from .models import TestModel


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name'
    )
    list_display_links = (
        'pk',
    )
