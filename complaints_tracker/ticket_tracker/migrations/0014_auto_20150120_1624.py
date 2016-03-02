# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_tracker', '0013_auto_20150120_1454'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketregister',
            options={'default_permissions': [], 'permissions': (('can_assign_ticket', 'Can Assign Ticket'), ('self_assign_ticket', 'Self Assign Ticket'), ('view_ticket_tracker', 'View Ticket Tracker'))},
        ),
    ]
