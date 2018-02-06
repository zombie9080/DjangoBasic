from django.db import models
from django.contrib import admin


# Here some specific query managers class that inherit from models.Manager are defined for this project,
# in defination of which the function get_queryset is overwritten for engage the capability of a filter,
# which used for removing records that are deleted logically from query set

# A basic manager class is defined here, for further inheritance
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
