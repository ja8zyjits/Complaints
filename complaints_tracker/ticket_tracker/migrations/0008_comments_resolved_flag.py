# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_tracker', '0007_auto_20150116_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='resolved_flag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
