from django.contrib import admin

# Register your models here.
from app.models import Plant, Report

admin.site.register(Plant)
admin.site.register(Report)
