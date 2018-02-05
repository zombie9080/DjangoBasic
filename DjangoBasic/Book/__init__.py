from django.db import models
from django.contrib import admin


class BaseManager(models.Manager):
    def get_queryset(self):
        query_dict = super(BaseManager, self).get_queryset().filter(isDelete=False)
        return query_dict


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['name', 'id']
    list_display_links = ['name']
    actions_on_bottom = True
    list_filter = ['name']
    search_fields = ['name']
