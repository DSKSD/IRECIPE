# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-13 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_auto_20170112_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialog',
            name='recom',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.RecomLog'),
        ),
    ]
