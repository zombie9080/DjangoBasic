from django.db import models
from Book import BaseManager


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=20, verbose_name='书名')
    pub_date = models.DateField(null=True, verbose_name='出版日期')
    readcount = models.IntegerField(default=0, verbose_name='阅读数')
    commentcount = models.IntegerField(default=0, verbose_name='评论数')
    isDelete = models.BooleanField(default=False, verbose_name='展示')

    books = BaseManager()

    class Meta:
        db_table = 'book'

    def readers_no_comment(self):
        return self.readcount - self.commentcount

    readers_no_comment.short_description = '未评论人数'
    readers_no_comment.admin_order_field = 'readcount'


class Role(models.Model):
    name = models.CharField(max_length=20)
    gender = models.BooleanField(default=True)
    description = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    book = models.ForeignKey(Book, on_delete=False)

    roles = BaseManager()

    class Meta:
        db_table = 'role'


class Area(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'area'


class CostomizedImage(models.Model):
    path = models.ImageField(upload_to='Book/', verbose_name='图片路径')

    class Meta:
        db_table = 'image'
