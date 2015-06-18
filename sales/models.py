# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tvr(models.Model):
  prz_g1 = models.CharField(max_length=255, blank=True, null=True)
  prz_g2 = models.CharField(max_length=255, blank=True, null=True)
  typ    = models.CharField(max_length=255, blank=True, null=True)
  nam    = models.CharField(max_length=255, blank=True, null=True)
  k      = models.FloatField(blank=True, null=True,default=0)
  c1     = models.FloatField(blank=True, null=True,default=0)
  c2     = models.FloatField(blank=True, null=True,default=0)
  c3     = models.FloatField(blank=True, null=True,default=0)
  c4     = models.FloatField(blank=True, null=True,default=0)

class StaticContent(models.Model):
  nam = models.CharField(primary_key=True, max_length=255)
  val = models.TextField(blank=True, null=True)

class Nkls(models.Model):
  date      = models.DateTimeField(auto_now_add=True)
  user      = models.ForeignKey(User)
  client    = models.CharField(max_length=255, blank=True, null=True, default=0)
  downloads = models.IntegerField(blank=True, null=True)
  val       = models.TextField(blank=True, null=True)