# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

admin.site.register(models.Article)
admin.site.register(models.Reporter)
