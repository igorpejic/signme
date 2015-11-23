# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import restful.models


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0009_auto_20150326_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='sign_pic',
            field=models.ImageField(null=True, upload_to=restful.models.get_image_path, blank=True),
            preserve_default=True,
        ),
    ]
