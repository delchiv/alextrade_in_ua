# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Nkls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('client', models.CharField(default=0, max_length=255, null=True, blank=True)),
                ('downloads', models.IntegerField(null=True, blank=True)),
                ('val', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaticContent',
            fields=[
                ('nam', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('val', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tvr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prz_g1', models.CharField(max_length=255, null=True, blank=True)),
                ('prz_g2', models.CharField(max_length=255, null=True, blank=True)),
                ('typ', models.CharField(max_length=255, null=True, blank=True)),
                ('nam', models.CharField(max_length=255, null=True, blank=True)),
                ('k', models.FloatField(default=0, null=True, blank=True)),
                ('c1', models.FloatField(default=0, null=True, blank=True)),
                ('c2', models.FloatField(default=0, null=True, blank=True)),
                ('c3', models.FloatField(default=0, null=True, blank=True)),
                ('c4', models.FloatField(default=0, null=True, blank=True)),
            ],
        ),
    ]
