# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0011_auto_20150327_2142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sign',
            options={'ordering': ['status']},
        ),
        migrations.AlterField(
            model_name='student',
            name='beer',
            field=models.IntegerField(default=10),
        ),
    ]
