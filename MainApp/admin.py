from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = '细胞房制度及档案文库系统后台'
admin.site.site_title = '细胞房制度及档案文库系统'


class FileAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('type', 'state')
    list_display_links = ('type', 'state')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'text',)
    list_display_links = ('date', 'user', 'text',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('register_time', 'name', 'student_id', 'phone', 'email', 'supervisor')
    list_display_links = ('register_time', 'name', 'student_id', 'phone', 'email', 'supervisor')


class TankCellAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'basket', 'floor', 'row', 'column')
    list_display_links = ('date', 'user', 'basket', 'floor', 'row', 'column')


class TankCellHistoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'get_user_name')
    list_display_links = ('date', 'get_user_name')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'file')
    list_display_links = ('name', 'group', 'file')


class UnitGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


admin.site.register(File, FileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(TankCell, TankCellAdmin)
admin.site.register(TankCellHistory, TankCellHistoryAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(UnitGroup, UnitGroupAdmin)
