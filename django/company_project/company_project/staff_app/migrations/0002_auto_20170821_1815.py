# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='staff_id',
            field=models.UUIDField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
