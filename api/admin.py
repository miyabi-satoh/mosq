from django.contrib import admin
from . import models


admin.site.register(models.Grade)
admin.site.register(models.Unit)
admin.site.register(models.Question)
admin.site.register(models.PrintHead)
admin.site.register(models.PrintDetail)
admin.site.register(models.Archive)
