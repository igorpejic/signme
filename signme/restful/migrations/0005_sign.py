# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0004_auto_20150314_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0)),
                ('lecture', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(to='restful.Lecture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
