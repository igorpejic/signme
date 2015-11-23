# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0008_student_beers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='beers',
            new_name='beer',
        ),
    ]
