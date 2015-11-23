# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0005_sign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='student_want_sign',
        ),
    ]
