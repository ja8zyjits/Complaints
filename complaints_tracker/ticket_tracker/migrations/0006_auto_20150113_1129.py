# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_tracker', '0005_complaintsregister_ipaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaintsregister',
            name='system_id',
            field=models.CharField(max_length=45),
            preserve_default=True,
        ),
    ]
