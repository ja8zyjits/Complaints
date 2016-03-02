# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_tracker', '0003_complaintsregister_email_msg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaintsregister',
            name='email_msg_id',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
