# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0003_auto_20150314_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='lectures',
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='students',
        ),
        migrations.DeleteModel(
            name='Faculty',
        ),
    ]
