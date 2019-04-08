# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Box(models.Model):
	length = models.FloatField()
	breadth = models.FloatField()
	height = models.FloatField()
	area = models.FloatField()
	volume = models.FloatField()
	created_by = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		# save area and volume
		self.area = self.length * self.breadth
		self.volume = self.length * self.breadth * self.height
		return super(Box, self).save(*args, **kwargs)

	# def __init__(self):
	# 	return "length: {} breadth: {} height: {} By {}".format(
	# 		self.length, self.breadth, self.height,
	# 		self.created_by.username
	# 	)


class ConditionParameter(models.Model):
	name = models.CharField(max_length=64)
	value = models.FloatField()

	# def __init__(self):
	# 	return self.name
