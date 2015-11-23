# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0002_auto_20150314_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='group',
            field=models.ForeignKey(to='auth.Group', null=True),
        ),
    ]
