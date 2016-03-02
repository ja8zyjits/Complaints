# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_tracker', '0011_auto_20150120_1229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketregister',
            options={'default_permissions': [], 'permissions': (('can_assign_task', 'Admin can assign new task to any engineer'), ('can_self_assign_task', 'Engineer can assign task to self only'), ('can_only_view', 'User can only view and change status of the issue'))},
        ),
    ]
