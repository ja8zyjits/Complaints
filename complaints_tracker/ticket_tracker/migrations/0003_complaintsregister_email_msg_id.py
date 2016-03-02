# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_tracker', '0002_comments_commentor'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaintsregister',
            name='email_msg_id',
            field=models.TextField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
