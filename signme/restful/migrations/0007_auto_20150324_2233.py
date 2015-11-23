# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0006_remove_lecture_student_want_sign'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='student_want_sign',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='restful.Sign', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sign',
            name='lecture',
            field=models.ForeignKey(to='restful.Lecture'),
        ),
        migrations.AlterField(
            model_name='sign',
            name='student',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
