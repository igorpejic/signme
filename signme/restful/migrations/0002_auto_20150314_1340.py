# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecture',
            old_name='groups',
            new_name='group',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='students_want_sign',
        ),
        migrations.AddField(
            model_name='lecture',
            name='student_want_sign',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
