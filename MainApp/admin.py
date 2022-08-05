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


admin.site.register(File, FileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
admin.site.register(Instrument, InstrumentAdmin)
