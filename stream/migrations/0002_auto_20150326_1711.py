# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_desc',
            field=models.CharField(default='', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
            preserve_default=True,
        ),
    ]
