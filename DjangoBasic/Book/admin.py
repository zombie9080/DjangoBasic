from Book.models import Book, Role, Area, CostomizedImage
from django.contrib import admin
from Book import BaseAdmin


# Register your models here.

# Here all models that could be controlled by administrators are registered,
# which means an administrator, who could be created by a shell command 'python manage.py createsuperuser',
# are granted the permission on the models registered here

class RoleSubInLine(admin.TabularInline):
    model = Role
    extra = 5


class BookAdmin(BaseAdmin):
    fieldsets = [
        ('基本信息', {'fields': ['name', 'pub_date']}),
        ('阅读信息', {'fields': ['readcount', 'commentcount']}),
        ('取消展示', {'fields': ['isDelete']})
    ]
    list_display = ['name', 'readcount', 'isDelete', 'readers_no_comment']
    inlines = [RoleSubInLine]


class RoleAdmin(BaseAdmin):
    list_display = ['name', 'id', 'gender', 'isDelete']


class AreaSubInLine(admin.TabularInline):
    model = Area
    extra = 5


class AreaAdmin(BaseAdmin):
    list_display = ['id', 'name', 'parent']
    fieldsets = [
        ('上级行政区', {'fields': ['parent']}),
        ('地区名', {'fields': ['name']})
    ]
    inlines = [AreaSubInLine]


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(CostomizedImage)
