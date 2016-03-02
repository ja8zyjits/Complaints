# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket_tracker', '0006_auto_20150113_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaintsregister',
            name='resolved_by',
            field=models.ForeignKey(related_name='resolved_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='complaintsregister',
            name='engineers',
            field=models.ForeignKey(related_name='assigned_to', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
