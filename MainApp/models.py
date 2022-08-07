from django.db import models
from django.conf import settings


# Create your models here.

class User(models.Model):
    student_id = models.CharField('学号', max_length=32, unique=True)
    name = models.CharField('姓名', max_length=32)
    phone = models.CharField('电话号码', max_length=32, unique=True)
    email = models.EmailField('邮箱', max_length=128, unique=True)
    supervisor = models.CharField('导师', max_length=32)
    password = models.CharField('密码', max_length=128)
    register_time = models.DateTimeField('注册时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-register_time"]
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class File(models.Model):
    title = models.CharField('标题', max_length=256)
    path = models.FileField('路径', upload_to='./download', null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'file'
        verbose_name = "文件"
        verbose_name_plural = verbose_name


class Instrument(models.Model):
    TYPE = (
        ('sterilizer', '灭菌锅'),
        ('centrifuge', '离心机'),
        ('safe', '生物安全柜'),
        ('incubator', '细胞培养箱'),
        ('cylinder', '二氧化碳钢瓶'),
        ('tank', '液氮罐'),
    )
    type = models.CharField('仪器类型', choices=TYPE, max_length=32)
    state = models.CharField('仪器状态', max_length=32)
    instruction = models.ForeignKey(File, related_name='instrument_instruction', on_delete=models.CASCADE)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = '仪器'
        verbose_name_plural = verbose_name
        ordering = ['type', ]


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE)
    date = models.DateField('评论日期', auto_now_add=True)
    text = models.CharField('评论内容', max_length=4096)

    def __str__(self):
        return '{}'.format(self.user_id)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['user', '-date']
