from django.db import models
from Book import BaseManager


# Models are created here.
# Once defination finished, migrations need to be detected and executed for generating table in database.
class Book(models.Model):
    # the argument verbose_name decides the description for its column in administrator's page
    name = models.CharField(max_length=20, verbose_name='书名')
    pub_date = models.DateField(null=True, verbose_name='出版日期')
    readcount = models.IntegerField(default=0, verbose_name='阅读数')
    commentcount = models.IntegerField(default=0, verbose_name='评论数')
    isDelete = models.BooleanField(default=False, verbose_name='展示')

    # An instance of base manager
    books = BaseManager()

    # Meta options allow you to customize your model, here it change the table name for our model in database.
    class Meta:
        db_table = 'book'

    # A model function.
    def readers_no_comment(self):
        return self.readcount - self.commentcount

    # Model function's option for displaying in administrator's page, which defined above
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


# A model for management on images uploaded by visitors.
class CostomizedImage(models.Model):
    # Path for storage of iamges uploaded.
    path = models.ImageField(upload_to='Book/', verbose_name='图片路径')

    class Meta:
        db_table = 'image'
