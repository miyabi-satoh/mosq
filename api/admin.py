from django.contrib import admin
from django.utils.html import format_html
from . import models


class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade_text', 'grade_code', 'id')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_text', 'unit_code', 'grade', 'id')
    list_filter = ['grade']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'answer_text',
                    'unit', 'source_text', 'url_link', 'id')
    list_filter = ['unit']

    @admin.display(description='参照')
    def url_link(self, obj):
        if obj.url_text:
            return format_html(
                '<a href="{}" target="_blank">Open</a>',
                obj.url_text)
        else:
            return ''


class PrintTypeAdmin(admin.ModelAdmin):
    list_display = ('type_text', 'template', 'cover', 'id')


class PrintHeadAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_questions', 'id')


class PrintDetailAdmin(admin.ModelAdmin):
    list_display = ('unit', 'quantity', 'printhead', 'id')
    list_filter = ['printhead']


class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'file', 'id')


admin.site.register(models.Grade, GradeAdmin)
admin.site.register(models.Unit, UnitAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.PrintType, PrintTypeAdmin)
admin.site.register(models.PrintHead, PrintHeadAdmin)
admin.site.register(models.PrintDetail, PrintDetailAdmin)
admin.site.register(models.Archive, ArchiveAdmin)
