from django.contrib import admin

# Register your models here.
from one import models
from django.contrib import admin
from .models import Problem

#admin.site.register(models.Problem)

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id','describe','opA','opB','opC','opD','answer')