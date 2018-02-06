from django.db import models
from django.contrib import admin


# Here some base admin, manager models are defined for further customized inheritance


# A basic manager class is defined here, for further inheritance
class BaseManager(models.Manager):
    def get_queryset(self):
        # Here the defination of function get_queryset is overwritten for engage the capability of a filter,
        # which used for removing records that are deleted logically from query set
        query_dict = super(BaseManager, self).get_queryset().filter(isDelete=False)
        return query_dict


# A basic admin class is defined here, for further inheritance
# Offers some basic user-friendly improvement in administrator page
class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['name', 'id']
    list_display_links = ['name']
    actions_on_bottom = True
    list_filter = ['name']
    # Search window defined
    search_fields = ['name']
