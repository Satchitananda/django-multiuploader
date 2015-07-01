# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiuploader.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MultiuploaderFile',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('filename', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField()),
                ('file', models.FileField(max_length=255, upload_to=multiuploader.utils._upload_to)),
            ],
            options={
                'verbose_name': 'multiuploader file',
                'verbose_name_plural': 'multiuploader files',
            },
        ),
    ]
