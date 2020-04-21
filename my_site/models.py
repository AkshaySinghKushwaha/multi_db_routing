# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserDatabases(models.Model):
	user 			= models.ForeignKey(User, on_delete = models.CASCADE)
	database_list 	= models.CharField(max_length = 300,default = None,blank = True)


class Product(models.Model):
	username_association	= models.CharField(max_length = 300,default = None	)	
	name 					= models.CharField(max_length = 300)
	slug 					= models.SlugField(max_length = 150,default = None,blank = True)
	description 			= models.TextField(default = None,blank = True)
	price 					= models.DecimalField(max_digits = 6,decimal_places = 2,default = 0.0,blank = True)

