from django.db import models


# Create your models here.

class User(models.Model):
    student_id = models.CharField('学号', max_length=256, unique=True)
    name = models.CharField('姓名', max_length=256)
    phone = models.CharField('电话号码', max_length=1024, unique=True)
    email = models.EmailField('邮箱', max_length=1024, unique=True)
    supervisor = models.CharField('导师', max_length=256)
    password = models.CharField('密码', max_length=1024)
    register_time = models.DateTimeField('注册时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-register_time"]
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class File(models.Model):
    title = models.CharField('标题', max_length=1024)
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
    type = models.CharField('仪器类型', choices=TYPE, max_length=256)
    state = models.CharField('仪器状态', max_length=256)
    instruction = models.ForeignKey(File, related_name='instrument_instruction', on_delete=models.CASCADE)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = '仪器'
        verbose_name_plural = verbose_name
        ordering = ['type', ]


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE)
    date = models.DateTimeField('留言日期', auto_now_add=True)
    text = models.CharField('留言内容', max_length=4096)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name
        ordering = ['user', '-date']


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, related_name='留言回复', on_delete=models.CASCADE)
    date = models.DateTimeField('回复日期', auto_now_add=True)
    text = models.TextField


class TankCell(models.Model):
    STATES = (
        ('占用', 'taken'),
        ('空闲', 'free')
    )
    name = models.CharField('名称', max_length=1024)
    special_attr = models.CharField('特殊属性', max_length=1024)
    user = models.ForeignKey(User, related_name='cell_user', on_delete=models.CASCADE)
    state = models.CharField('状态', choices=STATES, max_length=32)
    date = models.DateTimeField('取/放时间', auto_now=True)
    basket = models.DecimalField('篮子编号', max_digits=1, decimal_places=0)
    floor = models.DecimalField('层数编号', max_digits=1, decimal_places=0)
    row = models.DecimalField('行编号', max_digits=1, decimal_places=0)
    column = models.DecimalField('列编号', max_digits=1, decimal_places=0)

    def __str__(self):
        A = ['A', 'B', 'C', 'D']
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        return '{}罐{}层{}行{}列'.format(A[int(self.basket)], self.floor, self.row, a[int(self.column)])

    class Meta:
        verbose_name = '液氮罐'
        verbose_name_plural = verbose_name
        ordering = ['user', '-date']


class TankCellHistory(models.Model):
    tankCell = models.ForeignKey(TankCell, related_name='tank_cell', on_delete=models.CASCADE)
    date = models.DateTimeField('记录时间', auto_now=True)

    def user(self):
        return self.tankCell.user

    def cell(self):
        return self.tankCell

    def __str__(self):
        return '{}'.format(self.tankCell.user_id)

    class Meta:
        verbose_name = '液氮罐操作历史记录'
        verbose_name_plural = verbose_name
        ordering = ['-date', 'tankCell']


class UnitGroup(models.Model):
    name = models.CharField('名称', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '单元组'
        verbose_name_plural = verbose_name


class Unit(models.Model):
    name = models.CharField('名称', max_length=128)
    file = models.ForeignKey(File, related_name='file', on_delete=models.PROTECT)
    group = models.ForeignKey(UnitGroup, related_name='unit_group', on_delete=models.PROTECT)
    content = models.TextField('内容')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '单元'
        verbose_name_plural = verbose_name
