# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0007_auto_20150324_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='beers',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
