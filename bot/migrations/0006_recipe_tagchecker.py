# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-11 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20170111_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tagchecker',
            field=models.CharField(max_length=300, null=True),
        ),
    ]