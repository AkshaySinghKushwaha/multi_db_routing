# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from my_site.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)