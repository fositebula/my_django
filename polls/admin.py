# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

# Register your models here.
#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = models.Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    fieldsets = [
        ('question',                  {'fields':['question_text']}),
        ('Date Information',    {'fields':['pub_date'], 'classes':['collapse']})
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date', 'question_text']
admin.site.register(models.Question, QuestionAdmin)
#admin.site.register(models.Choice)