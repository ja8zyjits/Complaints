# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_tracker', '0014_auto_20150120_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketregister',
            name='created_by',
            field=models.ForeignKey(related_name='created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
