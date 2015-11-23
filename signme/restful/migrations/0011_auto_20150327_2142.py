# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0010_student_sign_pic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lecture',
            options={'ordering': ['start_hour']},
        ),
    ]
